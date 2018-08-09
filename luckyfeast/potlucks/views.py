from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Event, Dish_Type_Main, Guest_Instance, Event_Dish_Tally, Assignment
import datetime

def index(request):
    request.session['target_view'] = 'potlucks:event_index'
    if request.user_agent.is_mobile:
        browser_string = "This is a mobile browser"
        request.session['browser'] = 'mobile'
    else:
        browser_string = "This is a desktop browser"
        request.session['browser'] = 'desktop'
    context = {'browser': browser_string}
    return render(request, 'potlucks/desktop/index.html', context)

def user_login(request):
    request.session['target_view'] = 'potlucks:event_index'
    return render(request, 'potlucks/desktop/user_login.html')

def user_logout(request):
    logout(request)
    if request.user_agent.is_mobile:
        browser_string = "This is a mobile browser"
        request.session['browser'] = 'mobile'
    else:
        browser_string = "This is a desktop browser"
        request.session['browser'] = 'desktop'
    request.session['target_view'] = 'potlucks:event_index'
    return render(request, 'potlucks/desktop/index.html')

def user_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse(request.session['target_view']))
    else:
        context = {'error_message': "User and/or password not found"}
        return render(request, 'potlucks/desktop/user_login.html', context)

def user_register(request):
    user_list = User.objects.all()
    browser_string = request.session['browser']
    context = {'user_list': user_list, 'browser': browser_string}
    return render(request, 'potlucks/desktop/user_register.html', context)

def validate_username(request):
    user_name = request.GET.get('username', None)
    data = {
        'in_use': User.objects.filter(username__iexact=user_name).exists()
    }
    return JsonResponse(data)

def user_enter(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    user = User.objects.create_user(username, email, password)
    if request.POST['firstname'] != "":
        user.first_name = request.POST['firstname']
        user.save()
    if request.POST['lastname'] != "":
        user.last_name = request.POST['lastname']
        user.save()
    login(request, user)
    
    #Resolve any guest_instances for matching email
    instance_list = Guest_Instance.objects.filter(email=email)
    for instance in instance_list:
        instance.guest = user
        instance.save()
    return HttpResponseRedirect(reverse(request.session['target_view']))

def user_profile(request):
    return render(request, 'potlucks/desktop/user_profile.html')

def event_index(request):
    if not request.user.is_authenticated:
        request.session['target_view'] = 'potlucks:event_index'
        return render(request, 'potlucks/desktop/user_login.html')
    user = request.user
    event_list = user.event_set.all()
    invited_list = user.guest_instance_set.all()
    context = {'event_list': event_list, 'invited_list': invited_list}
    return render(request, 'potlucks/desktop/event_index.html', context)

def create_event(request):
    if not request.user.is_authenticated:
        request.session['target_view'] = 'potlucks:create_event'
        return render(request, 'potlucks/desktop/user_login.html')
    context = {'days':range(1, 32), 'hours':range(12), 'minutes':range(60)}
    return render(request, 'potlucks/desktop/create_event.html', context)

def event_details(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    user_dishes = Dish_Type_Main.objects.all()
    dish_tallies = Event_Dish_Tally.objects.get(event=event)
    if event.host != user:
        guest_instance = Guest_Instance.objects.get(event=event, guest=user)
        context = {'event': event, 'guest_instance': guest_instance, 'tallies': dish_tallies}
    else:
    	dish_types = Dish_Type_Main.objects.all()
    	context = {'event': event, 'dish_types':dish_types, 'tallies': dish_tallies}
    return render(request, 'potlucks/desktop/event_details.html', context)

#VIEW TO RENDER AFTER USER SUBMITS EVENT PARAMETERS
def event_enter(request):
    user = request.user
    event_name = request.POST['event_name']
    startDate = request.POST['start_date']
    startDate += ' ' + request.POST['start_time']
    formatString = '%m/%d/%Y %I:%M %p'
    start = datetime.datetime.strptime(startDate, formatString)
    
    endDate = request.POST['end_date']
    endDate += ' ' + request.POST['end_time']
    end = datetime.datetime.strptime(endDate, formatString)

    address = request.POST['address']
    #apt = request.POST['apt']
    #city = request.POST['city']
    #state = request.POST['state']
    #zipcode = request.POST['zipcode']

    #event = user.event_set.create(name=event_name, host=request.user, start_time=start, end_time=end, address=address, apt=apt, city=city, state=state, zipcode=zipcode)
    event = user.event_set.create(name=event_name, host=request.user, start_time=start, end_time=end, location=address)
    if request.POST['event_key'] != "":
        event.event_key = request.POST['event_key']
        event.save()
    dish_types = Dish_Type_Main.objects.all()
    tallies = event.event_dish_tally_set.create()
    tallies.save()
    context = {'event': event, 'dish_types': dish_types, 'tallies': tallies}
    return render(request, 'potlucks/desktop/event_details.html', context)

def validate_event_key(request):
    event_key = request.GET.get('eventkey', None)
    data = {
        'in_use': Event.objects.filter(event_key__iexact=event_key).exists()
    }
    return JsonResponse(data)

def event_cancel(request):
    event_id = request.POST['event_id']
    Event.objects.get(pk=event_id).delete()
    user = request.user
    event_list = user.event_set.all()
    invited_list = user.guest_instance_set.all()
    context = {'event_list': event_list, 'invited_list': invited_list}
    return render(request, 'potlucks/desktop/event_index.html', context)

def event_from_key(request):
    return render(request, 'potlucks/desktop/event_from_key.html')

def event_find(request):
    if Event.objects.filter(event_key__iexact=request.POST['event_key']).exists():
        event = Event.objects.get(event_key__iexact=request.POST['event_key'])
        if event.host.first_name.lower() == request.POST['host_name'].lower():
            dish_tallies = Event_Dish_Tally.objects.get(event=event)
            return render(request, 'potlucks/desktop/event_rsvp_invite.html', {'event': event, 'tallies': dish_tallies})
        else:
            context = {'error_message': 'Incorrect host'}
    else:
        context = {'error_message': 'Incorrect event'}
    return render(request, 'potlucks/desktop/event_from_key.html', context)

def event_rsvp_invite(request):
    event_id = request.POST['event_id']
    request.session['event_id'] = event_id
    if not request.user.is_authenticated:
        request.session['target_view'] = 'potlucks:event_rsvp_invite'
        context = {'error_message': "Please login before you continue"}
        return render(request, 'potlucks/desktop/user_login.html', context)
    event = Event.objects.get(pk=event_id)
    dish_tallies = Event_Dish_Tally.objects.get(event=event)
    context = {'event': event, 'tallies': dish_tallies}
    return render(request, 'potlucks/desktop/event_rsvp_invite.html', context)

def event_rsvp_action(request):
    if not request.user.is_authenticated:
        request.session['event_id'] = request.POST.get('event_id', '')
        request.session['target_view'] = 'potlucks:event_rsvp_action'
        request.session['rsvp'] = request.POST.get('rsvp', '')
        if request.session['rsvp'] == '2':
            request.session['dish_type'] = request.POST['dish_type']
            request.session['dish_name'] = request.POST['dish_name']
        context = {'error_message': "Please login before you continue"}
        return render(request, 'potlucks/desktop/user_login.html', context)
    
    user = request.user
    event_id = request.POST.get('event_id', '')
    if event_id == '':
        event_id = request.session['event_id']
    event = Event.objects.get(pk=event_id)

    if not event.guest_instance_set.filter(email=user.email).exists():
        event.guest_instance_set.create(email=user.email, guest=user)
    else:
        return HttpResponseRedirect(reverse('potlucks:event_index'))
    instance = event.guest_instance_set.get(email=user.email)
    if 'rsvp' not in request.POST:
        rsvp = request.session['rsvp']
    else:
        rsvp = request.POST['rsvp']
    instance.rsvp_status=int(rsvp)
    if rsvp == '2':
        dish_assigned = request.POST.get('dish_type', '')
        if dish_assigned == '':
            dish_assigned = request.session['dish_type']
        dish_name = request.POST.get('dish_name', '')
        if dish_name == '':
            dish_name = request.session['dish_name']
        tally = Event_Dish_Tally.objects.get(event=event)
        if dish_assigned == 'Appetizer':
            tally.app_assigned += 1
        if dish_assigned == 'Soup':
            tally.soup_assigned += 1
        if dish_assigned == 'Salad':
            tally.salad_assigned += 1
        if dish_assigned == 'Entree':
            tally.entree_assigned += 1
        if dish_assigned == 'Dessert':
            tally.dessert_assigned += 1
        if dish_assigned == 'Beverage':
            tally.beverage_assigned += 1
        tally.save()
        dish = Assignment( dish_type=dish_assigned, dish_name=dish_name, event=event)
        dish.assignment_status=True
        dish.save()
        event.rsvp_count += 1
        instance.assignment = dish
    instance.save()
    event.save()
    context = {'event': event, 'guest_instance': instance, 'tallies': tally}
    return render(request, 'potlucks/desktop/event_details.html', context)

def event_rsvp_change(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    instance = event.guest_instance_set.get(email=user.email)
    instance.rsvp_status=int(request.POST['rsvp'])
    if request.POST['rsvp'] == '3':
        assignment = instance.assignment
        assignment.assignment_status = False
        assignment.save()
        instance.assignment = None
    if request.POST['rsvp'] == '2':
        if instance.assignment is not None:
            instance.assignment.assignment_status = False;
            instance.assignment.save()
        dish_assigned = request.POST.get('dish_id', 0)
        dish = event.assignment_set.get(id=dish_assigned)
        dish.assignment_status=True
        dish.save()
        instance.assignment = dish
    instance.save()
    context = {'event': event, 'guest_instance': instance}
    return render(request, 'potlucks/desktop/event_details.html', context)

def event_dishes(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types':dish_types}
    return render(request, 'potlucks/desktop/event_dishes.html', context)

def event_add_guests(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    context = {'event': event}
    return render(request, 'potlucks/desktop/event_add_guests.html', context)

def event_add_dish(request):
    user = request.user
    event_id = request.POST['event_id']
    dish_added = request.POST['dish_main']
    event = Event.objects.get(pk=event_id)
    event.assignment_set.create(dish_type=dish_added)
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types': dish_types}
    return render( request, 'potlucks/desktop/event_details.html', context);

def event_add_dish_tallies(request):
    user = request.user
    event_id = request.POST['event_id']
    event = Event.objects.get(pk=event_id)
    app_count = request.POST['app_count']
    user_dishes = Dish_Type_Main.objects.all()
    dish_tallies = Event_Dish_Tally.objects.get(event=event)
    dish_tallies.app_needed = int(request.POST['app_count'])
    dish_tallies.soup_needed = int(request.POST['soup_count'])
    dish_tallies.salad_needed = int(request.POST['salad_count'])
    dish_tallies.entree_needed = int(request.POST['entree_count'])
    dish_tallies.dessert_needed = int(request.POST['dessert_count'])
    dish_tallies.beverage_needed = int(request.POST['beverage_count'])
    dish_tallies.save()
    if event.host != user:
        guest_instance = Guest_Instance.objects.get(event=event, guest=user)
        context = {'event': event, 'guest_instance': guest_instance, 'tallies': dish_tallies}
    else:
    	dish_types = Dish_Type_Main.objects.all()
    	context = {'event': event, 'dish_types':dish_types, 'tallies': dish_tallies}
    return render(request, 'potlucks/desktop/event_details.html', context);

def event_remove_dish(request):
    user = request.user
    event_id = request.POST['event_id']
    dish_removed = request.POST['dish_id']
    event = Event.objects.get(pk=event_id)
    dish = event.assignment_set.get(id=dish_removed)
    dish.delete()
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types': dish_types}
    return render( request, 'potlucks/desktop/event_details.html', context);

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
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types': dish_types}
    return render( request, 'potlucks/desktop/event_details.html', context);

def event_enter_guest(request):
    event_id = request.POST['id']
    event = Event.objects.get(pk=event_id)
    guest_email = request.POST['email']
    g_instance = event.guest_instance_set.create(email=guest_email)
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
    dish_types = Dish_Type_Main.objects.all()
    context = {'event': event, 'dish_types': dish_types}
    return render(request, 'potlucks/desktop/event_details.html', context)

# Create your views here.
