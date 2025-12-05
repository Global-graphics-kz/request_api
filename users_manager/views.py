from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import *
from .models import *

# Create your views here.

@csrf_exempt
def register_user(request):
    if request.method != 'POST':          
        return render(request, 'registration.html', {'form': UserRegistrationForm()})
    
    form = UserRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'registration.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

    instance = form.save()
    return HttpResponse(instance.id, status=status.HTTP_201_CREATED)

@csrf_exempt
def register_staff(request):
    if request.method != 'POST':          
        return render(request, 'registration.html', {'form': AdminRegistrationForm()})
    
    form = AdminRegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'registration.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

    instance = form.save()
    return HttpResponse(instance.id, status=status.HTTP_201_CREATED)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/requests/')
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'login.html')