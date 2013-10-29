from django.http import Http404
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('timeslots/home.html', {'poll': None})