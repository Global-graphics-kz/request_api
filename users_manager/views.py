from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .forms import *
from .models import *

# Create your views here.

def register_user(request):
    if request.method != 'POST':          
        return render(request, 'registration.html', {'form': UserRegistrationForm()})
    
    form = UserRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'registration.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

    instance = form.save()
    return Response(instance.id, status=status.HTTP_201_CREATED)

def register_staff(request):
    if request.method != 'POST':          
        return render(request, 'registration.html', {'form': AdminRegistrationForm()})
    
    form = AdminRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'registration.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

    instance = form.save()
    return Response(instance.id, status=status.HTTP_201_CREATED)
