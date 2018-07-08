from django.urls import path
from . import views

app_name = 'potlucks'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_auth', views.user_auth, name='user_auth'),
    path('user_register', views.user_register, name='user_register'),
    path('user_enter', views.user_enter, name='user_enter'),
    path('event_index', views.event_index, name='event_index'),
    path('create_event', views.create_event, name='create_event'),
    path('event_details', views.event_details, name='event_details'),
]
