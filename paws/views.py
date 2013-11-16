from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

def login(request):
    return render_to_response('paws/login.html', {'user': None})

def signup(request):
    return render_to_response('paws/signup.html', {'user': None})

def logout_view(request):
    logout(request)
    return redirect(reverse('timeslots_home'))