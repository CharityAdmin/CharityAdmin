import datetime
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata, Volunteer, VolunteerCommitment, VolunteerCommitmentException, VolunteerCommitmentMetadata, Event
from timeslots.forms import UserForm, ClientForm, VolunteerForm, VolunteerSignupForm, OpeningForm, CommitmentForm, OpeningExceptionForm, CommitmentExceptionForm

##
## VIEW UTILITY FUNCTIONS
##


def get_dates(request):
    """
    Utility function to return default start and end dates
    if they aren't provided in the URL parameters (or, eventually, via AJAX/Session variable)
    Standard default is startDate = now, endDate = defaultDays (see below) from now
    """
    from dateutil import parser

    defaultDays = 14

    startDate = request.GET.get('startdate')
    endDate = request.GET.get('enddate')

    if startDate:
        startDate = parser.parse(startDate)
    else:
        startDate = timezone.now()
    if endDate:
        endDate = parser.parse(endDate)
    else:
        endDate = timezone.now() + datetime.timedelta(days=defaultDays)

    return startDate, endDate


def get_volunteer(request, volunteerid=None):
    """
    Utility function to prevent us from Does Not Exist exception when trying to
    get a volunteer for a user who doesn't have one (this returns None)
    """
    volunteer = None
    if volunteerid and request.user.is_staff:
        volunteer = Volunteer.objects.get(user__id=volunteerid)
    else:
        try:
            volunteer = request.user.volunteer
        except Volunteer.DoesNotExist:
            pass
    return volunteer


##
## VIEWS
##


def home(request):
    return render(request, 'timeslots/home.html', {'poll': None})


def volunteer_signup(request):
    if request.method == "POST":
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: Decide if we want new users logged in after signing up. I don't think so, but if we do uncomment the next three lines
            # new_user = authenticate(username=form.cleaned_data['email'],
            #                         password=form.cleaned_data['password'])
            # login(request, new_user)
            return HttpResponseRedirect(reverse('timeslots_volunteer_signup_success'))
    else:
        form = VolunteerSignupForm()
    
    return render(request, 'timeslots/volunteer/volunteer_signup.html', { 'form': form })


def volunteer_signup_success(request):
    return render(request, 'timeslots/volunteer/volunteer_signup_success.html')

@login_required
def dashboard(request):
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    clients = None
    multipleclients = False
    opening_instances = list()
    opening_patterns = list()
    commitment_instances = list()

    if volunteer is not None:
        clients = volunteer.clients.all()
        if len(clients) > 1:
            multipleclients = True
        opening_instances = volunteer.get_unfilled_client_opening_instances(startDate=startDate, endDate=endDate)
        opening_patterns = volunteer.get_openings()
        commitment_instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)

    elif request.user.is_staff:
        clients = Client.objects.all()
        volunteers = Volunteer.objects.all()
        multipleclients = True
        opening_patterns = ClientOpening.objects.filter(Q(endDate__gte=timezone.now()) | Q(endDate__isnull=True), startDate__lte=timezone.now())
        for client in clients:
            opening_instances.extend(client.get_unfilled_opening_instances(startDate=startDate, endDate=endDate))
            opening_instances.sort(key=lambda item:item['date'])
        for volunteer in volunteers:
            commitment_instances.extend(volunteer.get_commitment_instances(startDate=startDate, endDate=endDate))
            commitment_instances.sort(key=lambda item:item['date'])

    return render(request, 'timeslots/dashboard.html', { "volunteer": volunteer, "clients": clients, "multipleclients": multipleclients, "opening_patterns": opening_patterns, "opening_instances": opening_instances, "commitment_instances": commitment_instances, "startDate": startDate, "endDate": endDate })


@login_required
def opening_instances_view(request, clientid=None):
    """ Show opening instances, or if a clientid is provided, opening instances for that client """
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    openings = list()
    client = None
    if volunteer is not None:
        if clientid:
            client = Client.objects.get(user__id=clientid)
            if not request.user.is_staff and client not in volunteer.clients.all():
                return HttpResponseForbidden
            openings = client.get_unfilled_opening_instances(startDate=startDate, endDate=endDate)
        else:
            openings = volunteer.get_unfilled_client_opening_instances(startDate=startDate, endDate=endDate)
    elif request.user.is_staff:
        for c in Client.objects.all():
            openings.extend(c.get_unfilled_opening_instances(startDate=startDate, endDate=endDate))
    openings.sort(key=lambda item:item['date'])

    return render(request, 'timeslots/opening/opening_instances_view.html', { "openings": openings, "client": client, "startDate": startDate, "endDate": endDate })


@login_required
def opening_pattern_view(request, openingid):
    """ Show a single opening pattern, along with instances based on startDate and endDate url parameters. """
    startDate, endDate = get_dates(request)

    opening = get_object_or_404(ClientOpening, id=openingid)
    is_myopening = True if opening.client.user == request.user else False
    instances = opening.get_instances(startDate=startDate, endDate=endDate)
    return render(request, 'timeslots/opening/opening_pattern_view.html', { "opening": opening, "is_myopening": is_myopening, "instances": instances, "startDate": startDate, "endDate": endDate })


@login_required
def opening_patterns_view(request, clientid=None, editlinks=False):
    """ Show a list of opening patterns. If clientid is specified, limit to that client. """
    client = None
    patterns = None
    if clientid:
        client = Client.objects.get(user__id=clientid)
    if client:
        if not request.user.is_staff and client not in volunteer.clients.all():
            return HttpResponseForbidden
        patterns = client.openings.all()
    elif request.user.is_staff:
        patterns = ClientOpening.objects.all()

    return render(request, 'timeslots/opening/opening_patterns_view.html', { "patterns": patterns, "client": client, "editlinks": editlinks })


@login_required
def opening_instance_view(request, clientid, year, month, day, time):
    """ Show a single opening instance """
    volunteer = get_volunteer(request)
    client = get_object_or_404(Client, user__id=clientid)
    opening = None
    openings = client.openings.all()
    instance_date = timezone.make_aware(datetime.datetime(int(year), int(month), int(day), int(time[0:2]), int(time[2:4])), timezone.UTC())
    for o in openings:
        instance = o.get_instance(instance_date)
        if instance:
            opening = o
            break

    if opening:
        exception_form = OpeningExceptionForm({ 'clientOpening': opening.id, 'date': instance_date })
    return render(request, 'timeslots/opening/opening_instance_view.html', { "instance_date": instance_date, "opening": opening, "client": client, "instance": instance, "exception_form": exception_form })

@login_required
def opening_add(request, clientid):
    """ create opening based on client userid and volunteer userid """
    if not request.user.is_staff:
        # only a staff member can create an opening for someone else
        client = request.user.client
    else:
        client = Client.objects.get(user__id=clientid)
    opening = ClientOpening.objects.create(client=client)
    return HttpResponseRedirect(reverse('timeslots_opening_edit', kwargs={'openingid': opening.id}))


@login_required
def opening_edit(request, openingid):
    opening = ClientOpening.objects.get(id=openingid)

    if not (request.user.is_staff or opening.client == request.user.client):
        # only a staff member can edit an opening for someone else
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = OpeningForm(request.POST, instance=opening)
        # metadataform = OpeningMetaDataForm(request.POST)
        if form.is_valid():
            # PROCESS DATA
            o = form.save()
            return HttpResponseRedirect(o.get_absolute_url())
    else:
        form = OpeningForm(instance=opening)
        # initial_metadata = {'clientOpening': opening.id, 'metadata': opening.get_all_metadata_string()}
        # metadataform = OpeningMetaDataForm(initial_metadata)

    return render(request, 'timeslots/opening/opening_edit.html', { 'opening': opening, 'form': form })


@staff_member_required
def opening_exception_view(request, openingid, year, month, day, time):
    """ View an opening exception, or add by POSTing """
    """ This view is odd because we don't actually want the user to see a form they can edit, the exception is created by clicking a link from another page """
    exception = None
    opening = None
    form = None
    if request.method == "POST":
        # We're adding a new exception
        form = OpeningExceptionForm(request.POST)
        if form.is_valid():
            opening = ClientOpening.objects.get(id=form.cleaned_data['clientOpening'])
            date = timezone.make_aware(form.cleaned_data['date'], timezone.UTC())
            exception, created = ClientOpeningException.objects.get_or_create(clientOpening=opening, date=date)
    if opening is None:
        opening = get_object_or_404(ClientOpening, id=openingid)
    if exception is None:
        date = timezone.make_aware(datetime.datetime(int(year), int(month), int(day), int(time[0:2]), int(time[2:4])), timezone.UTC())
        exception = get_object_or_404(ClientOpeningException, clientOpening=opening, date=date)
    if form is None:
        form = OpeningExceptionForm({ 'clientOpening': exception.clientOpening.id, 'date': exception.date })
    return render(request, 'timeslots/opening/opening_exception.html', { 'opening': opening, 'exception': exception, 'form': form })


@staff_member_required
def opening_exception_delete(request, openingid, year, month, day, time):
    """ Delete an opening exception """
    # opening = get_object_or_404(ClientOpening, id=openingid)
    # exceptiondate = timezone.make_aware(datetime.datetime(int(year), int(month), int(day), int(time[0:2]), int(time[2:4])), timezone.UTC())
    # exception = ClientOpeningException.objects.get(clientOpening=opening, date=exceptiondate)
    if request.method == "POST":
        # We're adding a new exception
        form = OpeningExceptionForm(request.POST)
        if form.is_valid():
            opening = ClientOpening.objects.get(id=form.cleaned_data['clientOpening'])
            date = form.cleaned_data['date']
            exception = ClientOpeningException.objects.get(clientOpening=opening, date=date)
            exception.delete()
            return HttpResponseRedirect(reverse('timeslots_opening_instance_view', kwargs={'clientid': opening.client.user.id, 'year':exception.date.year, 'month': exception.date.month, 'day': exception.date.day, 'time': exception.date.strftime('%H%M')}))
    raise Exception("Error while trying to delete an Opening Exception")


@login_required
def commitment_instances_view(request, clientid=None):
    """ Show commitment instances based on startDate and endDate url parameters. If clientid is specified, limit to that client """
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    client = None
    instances = list()
    if volunteer:
        if clientid:
            client = Client.objects.get(user__id=clientid)
            if not request.user.is_staff and client not in volunteer.clients.all():
                return HttpResponseForbidden
            instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate, client=client)
        else:
            instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)
    elif request.user.is_staff:
        volunteers = Volunteer.objects.all()
        for volunteer in volunteers:
            instances.extend(volunteer.get_commitment_instances(startDate=startDate, endDate=endDate))
            instances.sort(key=lambda item:item['date'])
    return render(request, 'timeslots/commitment/commitment_instances_view.html', { "instances": instances, "client": client, "startDate": startDate, "endDate": endDate })


@login_required
def commitment_patterns_view(request, clientid=None, editlinks=False, volunteerid=None):
    """ Show commitment patterns. If clientid is specified, limit to that client. If volunteerid is specified and user is staff, show that volunteer. """
    volunteer = get_volunteer(request, volunteerid)
    client = None
    patterns = None
    if clientid:
        client = Client.objects.get(user__id=clientid)
    if volunteer:
        if client:
            if not request.user.is_staff and client not in volunteer.clients.all():
                return HttpResponseForbidden
            patterns = volunteer.commitments.filter(clientOpening__client=client)
        else:
            patterns = volunteer.commitments.all()
    elif request.user.is_staff:
        if client:
            patterns = VolunteerCommitment.objects.filter(clientOpening__client=client)
        else:
            patterns = VolunteerCommitment.objects.all()

    return render(request, 'timeslots/commitment/commitment_patterns_view.html', { "patterns": patterns, "client": client, "editlinks": editlinks })


@login_required
def commitment_instance_view(request, clientid, year, month, day, time):
    """ Show a single commitment instance (i.e., a single date) """
    client = get_object_or_404(Client, user__id=clientid)
    commitment = None
    commitments = client.get_commitments()
    instance_date = timezone.make_aware(datetime.datetime(int(year), int(month), int(day), int(time[0:2]), int(time[2:4])), timezone.UTC())
    is_my_commitment = False
    for c in commitments:
        instance = c.get_instance(instance_date)
        if instance:
            commitment = c
            is_my_commitment = True if commitment.volunteer.user == request.user else False
            break
    if commitment:
        exception_form = CommitmentExceptionForm({ 'commitment': commitment.id, 'date': instance_date })

    return render(request, 'timeslots/commitment/commitment_instance_view.html', { "instance_date": instance_date, "commitment": commitment, "client": client, "instance": instance, "is_my_commitment": is_my_commitment, "exception_form": exception_form })


@login_required
def commitment_pattern_view(request, commitmentid):
    """ Show a single commitment pattern, along with instances based on startDate and endDate url parameters. """
    startDate, endDate = get_dates(request)

    commitment = get_object_or_404(VolunteerCommitment, id=commitmentid)
    is_my_commitment = True if commitment.volunteer.user == request.user else False
    instances = commitment.get_instances(startDate=startDate, endDate=endDate)
    return render(request, 'timeslots/commitment/commitment_pattern_view.html', { "commitment": commitment, "is_my_commitment": is_my_commitment, "instances": instances, "startDate": startDate, "endDate": endDate })


@login_required
def commitment_add(request, openingid, volunteerid=None):
    """ create commitment pattern based on openingid and volunteerid """
    if volunteerid and request.user.is_staff:
        # only a staff member can create a commitment for someone else
        volunteer = get_object_or_404(Volunteer, id=volunteerid)
    else:
        volunteer = request.user.volunteer
    opening = get_object_or_404(ClientOpening, id=openingid)
    commitment, created = VolunteerCommitment.objects.get_or_create(clientOpening=opening, volunteer=volunteer, type=opening.type)
    return HttpResponseRedirect(reverse('timeslots_commitment_edit', kwargs={'commitmentid': commitment.id}))

@login_required
def commitment_add_opening_select(request, volunteerid):
    if not (request.user.is_staff or request.user.id == volunteerid):
        # only staff members or the volunteer themselves
        return HttpResponseForbidden()

    if request.user.id == volunteerid:
        volunteer = request.user.volunteer
    else:
        volunteer = get_object_or_404(Volunteer, user__id=volunteerid)

    clients = volunteer.clients.all()

    if len(clients) == 1:
        openings = clients[0].openings.all()
        if len(openings) == 1:
            return HttpResponseRedirect(reverse('timeslots_commitment_add', kwargs={ 'openingid': openings[0].id, 'volunteerid': volunteer.id }))
    return render(request, 'timeslots/commitment/commitment_add_opening_select.html', { 'volunteer': volunteer, 'clients': clients })


@login_required
def commitment_edit(request, commitmentid):
    commitment = get_object_or_404(VolunteerCommitment, id=commitmentid)

    if not (request.user.is_staff or commitment.volunteer == request.user.volunteer):
        # only a staff member can edit a commitment for someone else
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommitmentForm(request.POST, instance=commitment)
        if form.is_valid():
            # PROCESS DATA
            c = form.save()
            return HttpResponseRedirect(c.get_absolute_url())
    else:
        form = CommitmentForm(instance=commitment)

    return render(request, 'timeslots/commitment/commitment_edit.html', { 'commitment': commitment, 'form': form })


@login_required
def commitment_exception_view(request, commitmentid, year, month, day, time):
    """ View a commitment exception, or add by POSTing """
    """ This view is odd because we don't actually want the user to see a form they can edit, the exception is created by clicking a link from another page """

    commitment = get_object_or_404(VolunteerCommitment, id=commitmentid)
    if not (request.user.is_staff or request.user.id == commitment.volunteer.user.id):
        # only a staff member or the committed volunteer can create a commitment exception
        return HttpResponseForbidden

    exception = None
    form = None
    if request.method == "POST":
        # We're adding a new exception
        form = CommitmentExceptionForm(request.POST)
        if form.is_valid():
            commitment = VolunteerCommitment.objects.get(id=form.cleaned_data['commitment'])
            date = timezone.make_aware(form.cleaned_data['date'], timezone.UTC())
            exception, created = VolunteerCommitmentException.objects.get_or_create(volunteerCommitment=commitment, date=date)

            #also create a new one-off opening
            opening = ClientOpening.objects.create(client=commitment.clientOpening.client, type="One-Off", startDate=date)
            ometadata = ClientOpeningMetadata.objects.create(clientOpening=opening, metadata=date.strftime('%Y-%m-%d'))
    if exception is None:
        date = timezone.make_aware(datetime.datetime(int(year), int(month), int(day), int(time[0:2]), int(time[2:4])), timezone.UTC())
        exception = get_object_or_404(VolunteerCommitmentException, volunteerCommitment=commitment, date=date)
    if form is None:
        form = CommitmentExceptionForm({ 'commitment': exception.volunteerCommitment.id, 'date': exception.date })
    return render(request, 'timeslots/commitment/commitment_exception.html', { 'commitment': commitment, 'exception': exception, 'form': form })


@login_required
def commitment_exception_delete(request, commitmentid, year, month, day, time):
    """ Delete a commitment exception """
    if request.method == "POST":
        # We're deleting the exception
        form = CommitmentExceptionForm(request.POST)
        if form.is_valid():
            commitment = VolunteerCommitment.objects.get(id=form.cleaned_data['commitment'])
            
            if not (request.user.is_staff or request.user.id == commitment.volunteer.user.id):
                # only a staff member or the committed volunteer can create a commitment exception
                return HttpResponseForbidden
            
            date = form.cleaned_data['date']
            exception = VolunteerCommitmentException.objects.get(volunteerCommitment=commitment, date=date)
            exception.delete()

            #also delete the one-off opening (metadata will be deleted by cascade)
            opening = ClientOpening.objects.filter(client=commitment.clientOpening.client, type="One-Off", metadata__metadata=date.strftime('%Y-%m-%d')).order_by("-id")[0]
            opening.delete()

            return HttpResponseRedirect(reverse('timeslots_commitment_instance_view', kwargs={'clientid': commitment.clientOpening.client.user.id, 'year':exception.date.year, 'month': exception.date.month, 'day': exception.date.day, 'time': exception.date.strftime('%H%M')}))
    raise Exception("Error while trying to delete a Commitment Exception")


@staff_member_required
def user_add(request, usertype):
    customererror = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # PROCESS DATA
            email = form.cleaned_data['email']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            user, usercreated = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': first, 'last_name': last, 'password': make_password(None)})

            if usertype == 'volunteer':
                # TODO: Send an email to the volunteer with a password reset link
                volunteer, typedusercreated = Volunteer.objects.get_or_create(user=user)
                redirectUrl = volunteer.get_absolute_edit_url()
            else:
                client, typedusercreated = Client.objects.get_or_create(user=user)
                redirectUrl = client.get_absolute_edit_url()

            # Whether or not we've created a new user, we want to send the admin to the edit page for that user (i.e., if they try to create a user who already exists, just show the dit screen)
            return HttpResponseRedirect(redirectUrl)
    else:
        form = UserForm()

    return render(request, 'timeslots/user_add.html', { "form": form, "usertype": usertype, "customererror": customererror })


@login_required
def client_view(request, userid):
    startDate, endDate = get_dates(request)
    volunteer = get_volunteer(request)
    client = get_object_or_404(Client, user__id=userid)
    openings = client.get_opening_instances(startDate=startDate, endDate=endDate)
    if volunteer:
        commitments = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate, client=client)
    else:
        commitments = None
    team = client.volunteers.all()
    return render(request, 'timeslots/client/client_view.html', { "client": client, "openings": openings, "commitments": commitments, "team": team, "startDate": startDate, "endDate": endDate  })


@staff_member_required
def clients_view(request):
    clients = Client.objects.all()
    return render(request, 'timeslots/list_view.html', { 'listObject': "Client", 'listItems': clients, 'addNewUrlName': 'timeslots_client_add' })


@staff_member_required
def client_edit(request, userid):
    client = Client.objects.get(user__id=userid)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(c.get_absolute_url())
    else:
        form = ClientForm(instance=client)

    return render(request, 'timeslots/client/client_edit.html', { "client": client, "form": form })


def volunteer_view(request, userid):
    startDate, endDate = get_dates(request)

    volunteer = get_object_or_404(Volunteer, user__id=userid)
    commitment_patterns = volunteer.get_current_commitments()
    commitment_instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)
    opening_patterns = volunteer.get_openings()

    return render(request, 'timeslots/volunteer/volunteer_view.html', { "volunteer": volunteer, "commitment_patterns": commitment_patterns, "commitment_instances": commitment_instances, "opening_patterns": opening_patterns, "startDate": startDate, "endDate": endDate })


@staff_member_required
def volunteers_view(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'timeslots/list_view.html', { 'listObject': "Volunteer", 'listItems': volunteers, 'addNewUrlName': 'timeslots_volunteer_add' })


@staff_member_required
def volunteer_edit(request, userid):
    volunteer = Volunteer.objects.get(user__id=userid)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            v = form.save()
            return HttpResponseRedirect(v.get_absolute_url())
    else:
        form = VolunteerForm(instance=volunteer)

    return render(request, 'timeslots/volunteer/volunteer_edit.html', { "volunteer": volunteer, "form": form })

@login_required
def event_add(request, clientid):
    if not request.user.is_staff:
        # only a staff member can create an opening for someone else
        client = request.user.client
    else:
        client = Client.objects.get(user__id=clientid)
    event = Event.objects.create(client=client)
    return HttpResponseRedirect(reverse('timeslots_event_edit', kwargs={'eventid': event.id}))

@login_required
def event_edit(request, eventid):
    event = Event.objects.get(id=eventid)

    # only a staff member can edit an opening for someone else
    if not (request.user.is_staff or event.client == request.user.client):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = OpeningForm(request.POST, instance=event)
        # metadataform = OpeningMetaDataForm(request.POST)
        if form.is_valid():
            # PROCESS DATA
            o = form.save()
            return HttpResponseRedirect(o.get_absolute_url())
    else:
        form = OpeningForm(instance=event)
        # initial_metadata = {'clientOpening': opening.id, 'metadata': opening.get_all_metadata_string()}
        # metadataform = OpeningMetaDataForm(initial_metadata)

    return render(request, 'timeslots/event/event_edit.html', { 'event': event, 'form': form })

@login_required
def event_view(request, eventid):

    event = get_object_or_404(Event, id=eventid)

    # only a staff member can edit an opening for someone else
    if not (request.user.is_staff or event.client == request.user.client):
        return HttpResponseForbidden()

    return render(request, 'timeslots/event/event_view.html', { "event": event })