import datetime
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata, Volunteer, VolunteerCommitment, VolunteerCommitmentException, VolunteerCommitmentMetadata
from timeslots.forms import UserForm, ClientForm, VolunteerForm, OpeningForm, OpeningMetaDataForm, CommitmentForm, CommitmentMetadataForm

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
    return render_to_response('timeslots/home.html', {'poll': None}, context_instance=RequestContext(request))


@login_required
def volunteer_dashboard(request):
    startDate, endDate = get_dates(request)

    volunteer = get_volunteer(request)
    clients = None
    openings = list()
    commitment_instances = list()

    if volunteer is not None:
        clients = volunteer.clients.all()
        for client in clients:
            openings.extend(client.get_unfilled_opening_instances(startDate=startDate, endDate=endDate))
        commitment_instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)

    return render_to_response('timeslots/volunteer_dashboard.html', { "volunteer": volunteer, "clients": clients, "openings": openings, "commitment_instances": commitment_instances, "startDate": startDate, "endDate": endDate }, context_instance=RequestContext(request))


@login_required
def openings_view(request):
    startDate, endDate = get_dates(request)

    volunteer = request.user.volunteer
    openings = list()
    if volunteer is not None:
        for client in volunteer.clients.all():
            openings.extend(client.get_unfilled_opening_instances(startDate=startDate, endDate=endDate))
    openings.sort(key=lambda item:item['date'])

    return render_to_response('timeslots/openings_view.html', { "openings": openings, "startDate": startDate, "endDate": endDate }, context_instance=RequestContext(request))


@login_required
def opening_view(request, openingid):
    """ Show a single opening, along with instances based on startDate and endDate url parameters. """
    startDate, endDate = get_dates(request)

    opening = ClientOpening.objects.get(id=openingid)
    is_myopening = True if opening.client.user == request.user else False
    instances = opening.get_instances(startDate=startDate, endDate=endDate)
    return render_to_response('timeslots/opening_view.html', { "opening": opening, "is_myopening": is_myopening, "instances": instances, "startDate": startDate, "endDate": endDate }, context_instance=RequestContext(request))


@login_required
def opening_add(request, clientid):
    """ create opening based on client userid and volunteer userid """
    if not request.user.is_staff:
        # only a staff member can create a opening for someone else
        client = request.user.client
    else:
        client = Client.objects.get(id=clientid)
    opening, created = ClientOpening.objects.get_or_create(client=client)
    return HttpResponseRedirect(reverse('timeslots_opening_edit', kwargs={'openingid': opening.id}))


@login_required
def opening_edit(request, openingid):
    opening = ClientOpening.objects.get(id=openingid)

    if not request.user.is_staff and opening.client is not request.user.client:
        # only a staff member can edit an opening for someone else
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = OpeningForm(request.POST, instance=opening)
        # metadataform = OpeningMetaDataForm(request.POST)
        if form.is_valid():
            # PROCESS DATA
            form.save()
            print "TIMESLOTS OPENING EDIT SUCCESS"
            HttpResponseRedirect(reverse('timeslots_opening_edit_success', kwargs={'openingid':opening.id}))
    else:
        form = OpeningForm(instance=opening)
        # initial_metadata = {'clientOpening': opening.id, 'metadata': opening.get_all_metadata_string()}
        # metadataform = OpeningMetaDataForm(initial_metadata)

    return render_to_response('timeslots/opening_edit.html', { 'opening': opening, 'form': form }, context_instance=RequestContext(request))


@staff_member_required
def opening_edit_success(request, openingid):
    opening = ClientOpening.objects.get(id=openingid)
    return render_to_response('timeslots/opening_edit_success.html', { "opening": opening }, context_instance=RequestContext(request))


@login_required
def commitments_view(request):
    """ Show commitments based on startDate and endDate url parameters. """
    startDate, endDate = get_dates(request)

    instances = request.user.volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)
    return render_to_response('timeslots/commitments_view.html', { "instances": instances, "startDate": startDate, "endDate": endDate }, context_instance=RequestContext(request))


@login_required
def commitment_view(request, commitmentid):
    """ Show a single commitment, along with instances based on startDate and endDate url parameters. """
    startDate, endDate = get_dates(request)

    commitment = VolunteerCommitment.objects.get(id=commitmentid)
    is_mycommitment = True if commitment.volunteer.user == request.user else False
    instances = commitment.get_instances(startDate=startDate, endDate=endDate)
    return render_to_response('timeslots/commitment_view.html', { "commitment": commitment, "is_mycommitment": is_mycommitment, "instances": instances, "startDate": startDate, "endDate": endDate }, context_instance=RequestContext(request))


@login_required
def commitment_add(request, openingid, volunteerid=None):
    """ create commitment based on openingid and volunteerid """
    if not request.user.is_staff:
        # only a staff member can create a commitment for someone else
        volunteer = request.user.volunteer
    else:
        volunteer = Volunteer.objects.get(id=volunteerid)
    opening = ClientOpening.objects.get(id=openingid)
    commitment, created = VolunteerCommitment.objects.get_or_create(clientopening=opening, volunteer=volunteer)
    return HttpResponseRedirect(reverse('timeslots_commitment_edit', kwargs={'commitmentid': commitment.id}))


@login_required
def commitment_edit(request, commitmentid):
    commitment = VolunteerCommitment.objects.get(id=commitmentid)

    if not request.user.is_staff and commitment.volunteer is not request.user.volunteer:
        # only a staff member can edit a commitment for someone else
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommitmentForm(request.POST, instance=commitment)
        if form.is_valid():
            # PROCESS DATA
            form.save()
            HttpResponseRedirect(reverse('timeslots_commitment_edit_success'))
    else:
        form = CommitmentForm(instance=commitment)

    return render_to_response('timeslots/commitment_edit.html', { 'commitment': commitment, 'form': form }, context_instance=RequestContext(request))


@staff_member_required
def commitment_edit_success(request, commitmentid):
    commitment = VolunteerCommitment.objects.get(id=commitmentid)
    return render_to_response('timeslots/commitment_edit_success.html', { "commitment": commitment }, context_instance=RequestContext(request))


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

    return render_to_response('timeslots/user_add.html', { "form": form, "customererror": customererror }, context_instance=RequestContext(request))


@login_required
def client_view(request, userid):
    startDate, endDate = get_dates(request)

    client = Client.objects.get(user__id=userid)
    openings = client.get_opening_instances(startDate=startDate, endDate=endDate)
    team = client.volunteers.all()
    return render_to_response('timeslots/client_view.html', { "client": client, "openings": openings, "team": team, "startDate": startDate, "endDate": endDate  }, context_instance=RequestContext(request))


@staff_member_required
def clients_view(request):
    clients = Client.objects.all()
    return render_to_response('timeslots/list_view.html', { 'listTitle': "Clients", 'listItems': clients }, context_instance=RequestContext(request))


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

    return render_to_response('timeslots/client_edit.html', { "client": client, "form": form }, context_instance=RequestContext(request))


@staff_member_required
def client_edit_success(request, userid):
    client = Client.objects.get(user__id=userid)
    return render_to_response('timeslots/client_edit_success.html', { "client": client }, context_instance=RequestContext(request))


def volunteer_view(request, userid):
    startDate, endDate = get_dates(request)

    volunteer = Volunteer.objects.get(user__id=userid)
    commitments = volunteer.get_current_commitments()
    instances = volunteer.get_commitment_instances(startDate=startDate, endDate=endDate)

    return render_to_response('timeslots/volunteer_view.html', { "volunteer": volunteer, "commitments": commitments, "instances": instances, "startDate": startDate, "endDate": endDate  }, context_instance=RequestContext(request))


@staff_member_required
def volunteers_view(request):
    volunteers = Volunteer.objects.all()
    return render_to_response('timeslots/list_view.html', { 'listTitle': "Volunteers", 'listItems': volunteers }, context_instance=RequestContext(request))


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

    return render_to_response('timeslots/volunteer_edit.html', { "volunteer": volunteer, "form": form }, context_instance=RequestContext(request))


@staff_member_required
def volunteer_edit_success(request, userid):
    volunteer = Volunteer.objects.get(user__id=userid)
    return render_to_response('timeslots/client_edit_success.html', { "volunteer": volunteer }, context_instance=RequestContext(request))
