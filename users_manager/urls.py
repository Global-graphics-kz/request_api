from django.urls import path
from .views import *

urlpatterns = [
    path('register/user/', register_user),
    path('register/staff/', register_staff),
]