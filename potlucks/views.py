from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'potlucks/index.html')

def user_login(request):
    return render(request, 'potlucks/user_login.html')

def user_auth(request):
    return render(request, 'potlucks/user_auth.html')

def user_register(request):
    return render(request, 'potlucks/user_register.html')

def user_enter(request):
    return render(request, 'potlucks/user_enter.html')

def event_index(request):
    return render(request, 'potlucks/event_index.html')

def create_event(request):
    return render(request, 'potlucks/create_event.html')

def event_details(request):
    return render(request, 'potlucks/event_details.html')

# Create your views here.
