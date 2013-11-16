from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from timeslots.models import Client, ClientOpening, ClientOpeningException, ClientOpeningMetadata

def home(request):
    return render_to_response('timeslots/home.html', {'poll': None})

@login_required
def volunteer_dashboard(request):
	volunteer = request.user.volunteer
	clients = None
	if volunteer is not None:
		clients = volunteer.clients.all()
	return render_to_response('timeslots/volunteer_dashboard.html', { "volunteer": volunteer, "clients": clients }, context_instance = RequestContext(request))

@login_required
def upcoming_openings(request):
	return render_to_response('timeslots/upcoming_openings.html', context_instance = RequestContext(request))

@login_required
def upcoming_commitments(request):
	return render_to_response('timeslots/upcoming_commitments.html', context_instance = RequestContext(request))

@login_required
def client_view(request, clientname):
	client = Client.objects.get(user__username=clientname)
	return render_to_response('timeslots/client_view.html', { "client": client }, context_instance = RequestContext(request))