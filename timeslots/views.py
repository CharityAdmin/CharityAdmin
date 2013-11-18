import datetime
from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import timezone
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata


def home(request):
    return render_to_response('timeslots/home.html', {'poll': None})


@login_required
def volunteer_dashboard(request):
    volunteer = request.user.volunteer
    clients = None
    if volunteer is not None:
        clients = volunteer.clients.all()
    return render_to_response('timeslots/volunteer_dashboard.html', { "clients": clients }, context_instance=RequestContext(request))


@login_required
def upcoming_openings(request):
    volunteer = request.user.volunteer
    openings = list()
    if volunteer is not None:
        endDate = timezone.now() + datetime.timedelta(days=30)
        for client in volunteer.clients.all():
            openings.extend(client.get_next_unfilled_opening_instances(endDate=endDate))
    openings.sort(key=lambda item:item['date'])
    return render_to_response('timeslots/upcoming_openings.html', { "openings": openings }, context_instance=RequestContext(request))


@login_required
def upcoming_commitments(request):
    commitments = request.user.volunteer.get_current_commitments()
    return render_to_response('timeslots/upcoming_commitments.html', { "commitments": commitments }, context_instance=RequestContext(request))


@login_required
def client_view(request, clientname):
    client = Client.objects.get(user__username=clientname)
    openings = client.get_next_opening_instances(endDate=timezone.now() + datetime.timedelta(days=30))
    return render_to_response('timeslots/client_view.html', { "client": client, "openings": openings }, context_instance=RequestContext(request))