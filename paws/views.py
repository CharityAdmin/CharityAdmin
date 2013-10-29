from django.http import Http404
from django.shortcuts import render_to_response

def login(request):
    return render_to_response('paws/login.html', {'user': None})

def signup(request):
    return render_to_response('paws/signup.html', {'user': None})