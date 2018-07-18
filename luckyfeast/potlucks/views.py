from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Event, Dish_Type_Main, Guest_Instance
import datetime

def index(request):
    if request.user_agent.is_mobile:
        browser_string = "This is a mobile browser"
        request.session['browser'] = 'mobile'
    else:
        browser_string = "This is a desktop browser"
        request.session['browser'] = 'desktop'
    context = {'browser': browser_string}
    return render(request, 'potlucks/index.html', context)

def user_login(request):
    request.session['target_view'] = 'potlucks:event_index'
    return render(request, 'potlucks/' + request.session['browser'] + '/user_login.html')

def user_logout(request):
    logout(request)
    return render(request, 'potlucks/index.html')

def user_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse(request.session['target_view']))
    else:
        context = {'error_message': "User and/or password not found"}
        return render(request, 'potlucks/user_login.html', context)

def user_register(request):
    userList = User.objects.all()
    context = {'userList': userList}
    return render(request, 'potlucks/user_register.html', context)

def user_enter(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    user = User.objects.create_user(username, email, password)
    login(request, user)
    
    #Resolve any guest_instances for matching email
    instance_list = Guest_Instance.objects.filter(email=email)
    for instance in instance_list:
        instance.guest = user
        instance.save()
    return render(request, 'potlucks/event_index.html')

def user_profile(request):
    return render(request, 'potlucks/user_profile.html')

def event_index(request):
    if not request.user.is_authenticated:
        request.session['target_view'] = 'potlucks:event_index'
        return render(request, 'potlucks/user_login.html')
    user = request.user
    event_list = user.event_set.all()
    invited_list = user.guest_instance_set.all()
    context = {'event_list': event_list, 'invited_list': invited_list}
    return render(request, 'potlucks/event_index.html', context)

def create_event(request):
    if not request.user.is_authenticated:
        request.session['target_view'] = 'potlucks:create_event'
        return render(request, 'potlucks/user_login.html')
    context = {'days':range(1, 32), 'hours':range(12), 'minutes':range(60)}
    return render(request, 'potlucks/create_event.html', context)

def event_details(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    context = {'event': event}
    return render(request, 'potlucks/event_details.html', context)

def event_enter(request):
    user = request.user
    event_name = request.POST['event_name']
    
    startMonth = request.POST['startMonth']
    startDate = request.POST['startDate']
    startYear = request.POST['startYear']
    startHour = int(request.POST['startHour'])
    startMinutes = request.POST['startMinutes']
    startAm = request.POST['startAm']
    if startAm == "pm":
        startHour += 12
    start = datetime.datetime(int(startYear), int(startMonth), int(startDate), int(startHour), int(startMinutes))    

    endMonth = request.POST['endMonth']
    endDate = request.POST['endDate']
    endYear = request.POST['endYear']
    endHour = int(request.POST['endHour'])
    endMinutes = request.POST['endMinutes']
    endAm = request.POST['endAm']
    if endAm == "pm":
        endHour += 12
    end = datetime.datetime(int(endYear), int(endMonth), int(endDate), int(endHour), int(endMinutes))    

    address = request.POST['address']
    apt = request.POST['apt']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']

    event = user.event_set.create(name=event_name, host=request.user, start_time=start, end_time=end, address=address, apt=apt, city=city, state=state, zipcode=zipcode)
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event}
    return render(request, 'potlucks/event_details.html', context)

def event_dishes(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types':dish_types}
    return render(request, 'potlucks/event_dishes.html', context)

def event_add_guests(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    context = {'event': event}
    return render(request, 'potlucks/event_add_guests.html', context)

def event_add_dish(request):
    user = request.user
    event_id = request.POST['event_id']
    dish_added = request.POST['dish_main']
    event = Event.objects.get(pk=event_id)
    event.assignment_set.create(dish_type=dish_added)
    context = {'event': event}
    return render( request, 'potlucks/event_details.html', context);

def event_remove_dish(request):
    user = request.user
    event_id = request.POST['event_id']
    dish_removed = request.POST['dish_id']
    event = Event.objects.get(pk=event_id)
    dish = event.assignment_set.get(id=dish_removed)
    dish.delete()
    context = {'event': event}
    return render( request, 'potlucks/event_details.html', context);

def event_assign_dish(request):
    user = request.user
    event_id = request.POST['event_id']
    dish_assigned = request.POST['dish_id']
    event = Event.objects.get(pk=event_id)
    dish = event.assignment_set.get(id=dish_assigned)
    dish.assignment_status=True
    dish.save()
    guest_instance=event.guest_instance_set.get(guest=user)
    guest_instance.assignment=dish
    guest_instance.save()
    context = {'event': event}
    return render( request, 'potlucks/event_details.html', context);

def event_enter_guest(request):
    event_id = request.POST['id']
    event = Event.objects.get(pk=event_id)
    guest_email = request.POST['email']
    g_instance = event.guest_instance_set.create(email=guest_email, rsvp_status=False)
    guest_user = User.objects.filter(email=guest_email)
    if guest_user.exists():
        guest_user = User.objects.get(email=guest_email)
        g_instance.guest=guest_user
        g_instance.save()
    #send_mail(
    #    request.user.username + 'invited you to an event!',
    #    'You have been invited to ' + event.name,
    #    'srossi455@gmail.com',
    #    [guest_email]
    #)
    context = {'event': event}
    return render(request, 'potlucks/event_details.html', context)

# Create your views here.
