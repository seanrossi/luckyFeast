from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'potlucks'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_loout', views.user_logout, name='user_logout'),
    path('user_auth', views.user_auth, name='user_auth'),
    path('user_register', views.user_register, name='user_register'),
    path('user_enter', views.user_enter, name='user_enter'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('event_index', views.event_index, name='event_index'),
    path('create_event', views.create_event, name='create_event'),
    path('event_details', views.event_details, name='event_details'),
    path('event_dishes', views.event_dishes, name='event_dishes'),
    path('event_enter', views.event_enter, name='event_enter'),
    path('event_add_guests', views.event_add_guests, name='event_add_guests'),
    path('event_add_dish', views.event_add_dish, name='event_add_dish'),
    path('event_remove_dish', views.event_remove_dish, name='event_remove_dish'),
    path('event_assign_dish', views.event_assign_dish, name='event_assign_dish'),
    path('event_enter_guest', views.event_enter_guest, name='event_enter_guest'),
    path('event_cancel', views.event_cancel, name='event_cancel'),
    path('event_find', views.event_find, name='event_find'),
    path('event_rsvp_invite', views.event_rsvp_invite, name='event_rsvp_invite'),
    path('event_rsvp_action', views.event_rsvp_action, name='event_rsvp_action'),
    path('event_rsvp_change', views.event_rsvp_change, name='event_rsvp_change'),
    path('key/', views.event_from_key, name='event_from_key'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]
