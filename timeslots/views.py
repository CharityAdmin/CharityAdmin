import datetime
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata, Volunteer, VolunteerCommitment, VolunteerCommitmentException, VolunteerCommitmentMetadata
from timeslots.forms import UserForm, ClientForm, VolunteerForm, OpeningForm, CommitmentForm

##
## VIEW UTILITY FUNCTIONS
##


def get_dates(request):
    """
    Utility function to return default start and end dates
    if they aren't provided in the URL parameters (or, eventually, via AJAX/Session variable)
    Standard default is startDate = now, endDate = 30 days from now
    """
    from dateutil import parser

    startDate = request.GET.get('startdate')
    endDate = request.GET.get('enddate')

    if startDate:
        startDate = parser.parse(startDate)
    else:
        startDate = timezone.now()
    if endDate:
        endDate = parser.parse(endDate)
    else:
        endDate = timezone.now() + datetime.timedelta(days=30)

    return startDate, endDate


def get_volunteer(request):
    """
    Utility function to prevent us from Does Not Exist exception when trying to
    get a volunteer for a user who doesn't have one (this returns None)
    """
    try:
        volunteer = request.user.volunteer
    except Volunteer.DoesNotExist:
        volunteer = None
    return volunteer


##
## VIEWS
##


def home(request):
    return render(request, 'timeslots/home.html', {'poll': None})


@login_required
def dashboard(request):
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    clients = None
    multipleclients = False
    openings = list()
    commitment_instances = list()

    if volunteer is not None:
        clients = volunteer.clients.all()
        if len(clients) > 1:
            multipleclients = True
        for client in clients:
            openings.extend(client.get_unfilled_opening_instances(startDate=startDate, endDate=endDate))
        commitment_instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)


    return render(request, 'timeslots/dashboard.html', { "volunteer": volunteer, "clients": clients, "multipleclients": multipleclients, "openings": openings, "commitment_instances": commitment_instances, "startDate": startDate, "endDate": endDate })


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
            for c in volunteer.clients.all():
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

    return render(request, 'timeslots/opening/opening_instance_view.html', { "instance_date": instance_date, "opening": opening, "client": client, "instance": instance })

@login_required
def opening_add(request, clientid):
    """ create opening based on client userid and volunteer userid """
    if not request.user.is_staff:
        # only a staff member can create a opening for someone else
        client = request.user.client
    else:
        client = Client.objects.get(user__id=clientid)
    opening, created = ClientOpening.objects.get_or_create(client=client)
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
            form.save()
            return HttpResponseRedirect(reverse('timeslots_opening_edit_success', kwargs={'openingid':opening.id}))
    else:
        form = OpeningForm(instance=opening)
        # initial_metadata = {'clientOpening': opening.id, 'metadata': opening.get_all_metadata_string()}
        # metadataform = OpeningMetaDataForm(initial_metadata)

    return render(request, 'timeslots/opening/opening_edit.html', { 'opening': opening, 'form': form })


@staff_member_required
def opening_edit_success(request, openingid):
    opening = ClientOpening.objects.get(id=openingid)
    return render(request, 'timeslots/opening/opening_edit_success.html', { "opening": opening })


@login_required
def commitment_instances_view(request, clientid=None):
    """ Show commitment instances based on startDate and endDate url parameters. If clientid is specified, limit to that client """
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    client = None
    if volunteer:
        if clientid:
            client = Client.objects.get(user__id=clientid)
            if not request.user.is_staff and client not in volunteer.clients.all():
                return HttpResponseForbidden
            instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate, client=client)
        else:
            instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)
    else:
        instances = list()
    return render(request, 'timeslots/commitment/commitment_instances_view.html', { "instances": instances, "client": client, "startDate": startDate, "endDate": endDate })


@login_required
def commitment_patterns_view(request, clientid=None):
    """ Show commitment patterns. If clientid is specified, limit to that client """
    volunteer = get_volunteer(request)
    client = None
    if volunteer:
        if clientid:
            client = Client.objects.get(user__id=clientid)
            if not request.user.is_staff and client not in volunteer.clients.all():
                return HttpResponseForbidden
            patterns = volunteer.commitments.filter(clientOpening__client=client)
        else:
            patterns = volunteer.commitments.all()
    else:
        instances = list()
    return render(request, 'timeslots/commitment/commitment_patterns_view.html', { "patterns": patterns, "client": client })


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

    return render(request, 'timeslots/commitment/commitment_instance_view.html', { "instance_date": instance_date, "commitment": commitment, "client": client, "instance": instance, "is_my_commitment": is_my_commitment })


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
    if not request.user.is_staff:
        # only a staff member can create a commitment for someone else
        volunteer = request.user.volunteer
    else:
        volunteer = get_object_or_404(Volunteer, id=volunteerid)
    opening = get_object_or_404(ClientOpening, id=openingid)
    commitment, created = VolunteerCommitment.objects.get_or_create(clientOpening=opening, volunteer=volunteer)
    return HttpResponseRedirect(reverse('timeslots_commitment_edit', kwargs={'commitmentid': commitment.id}))


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
            form.save()
            return HttpResponseRedirect(reverse('timeslots_commitment_edit_success', kwargs={'commitmentid': commitmentid}))
    else:
        form = CommitmentForm(instance=commitment)

    return render(request, 'timeslots/commitment/commitment_edit.html', { 'commitment': commitment, 'form': form })


@login_required
def commitment_edit_success(request, commitmentid):
    commitment = VolunteerCommitment.objects.get(id=commitmentid)
    return render(request, 'timeslots/commitment/commitment_edit_success.html', { "commitment": commitment })


@staff_member_required
def user_add(request):
    customererror = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # PROCESS DATA
            type = form.cleaned_data['type']
            email = form.cleaned_data['email']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            user, usercreated = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': first, 'last_name': last})

            if type == 'VOLUNTEER':
                volunteer, typedusercreated = Volunteer.objects.get_or_create(user=user)
                redirectUrl = reverse('timeslots_volunteer_edit', kwargs={'userid': user.id})
            else:
                client, typedusercreated = Client.objects.get_or_create(user=user)
                redirectUrl = reverse('timeslots_client_edit', kwargs={'userid': user.id})

            if typedusercreated:
                # SUCCESS
                return HttpResponseRedirect(redirectUrl)
            else:
                customererror = "Error: Email address %s already has an associated %s" % (email, type.lowercase())
    else:
        form = UserForm()

    return render(request, 'timeslots/user_add.html', { "form": form, "customererror": customererror })


@login_required
def client_view(request, userid):
    startDate, endDate = get_dates(request)

    client = get_object_or_404(Client, user__id=userid)
    openings = client.get_opening_instances(startDate=startDate, endDate=endDate)
    team = client.volunteers.all()
    return render(request, 'timeslots/client/client_view.html', { "client": client, "openings": openings, "team": team, "startDate": startDate, "endDate": endDate  })


@staff_member_required
def clients_view(request):
    clients = Client.objects.all()
    return render(request, 'timeslots/list_view.html', { 'listTitle': "Clients", 'listItems': clients })


@staff_member_required
def client_edit(request, userid):
    client = Client.objects.get(user__id=userid)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('timeslots_client_edit_success', kwargs={'userid': userid}))
    else:
        form = ClientForm(instance=client)

    return render(request, 'timeslots/client/client_edit.html', { "client": client, "form": form })


@staff_member_required
def client_edit_success(request, userid):
    client = Client.objects.get(user__id=userid)
    return render(request, 'timeslots/client/client_edit_success.html', { "client": client })


def volunteer_view(request, userid):
    startDate, endDate = get_dates(request)

    volunteer = get_object_or_404(Volunteer, user__id=userid)
    commitments = volunteer.get_current_commitments()
    instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)

    return render(request, 'timeslots/volunteer/volunteer_view.html', { "volunteer": volunteer, "commitments": commitments, "instances": instances, "startDate": startDate, "endDate": endDate  })


@staff_member_required
def volunteers_view(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'timeslots/list_view.html', { 'listTitle': "Volunteers", 'listItems': volunteers })


@staff_member_required
def volunteer_edit(request, userid):
    volunteer = Volunteer.objects.get(user__id=userid)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('timeslots_volunteer_edit_success', kwargs={'userid': userid}))
    else:
        form = VolunteerForm(instance=volunteer)

    return render(request, 'timeslots/volunteer/volunteer_edit.html', { "volunteer": volunteer, "form": form })


@staff_member_required
def volunteer_edit_success(request, userid):
    volunteer = Volunteer.objects.get(user__id=userid)
    return render(request, 'timeslots/client/volunteer_edit_success.html', { "volunteer": volunteer })
