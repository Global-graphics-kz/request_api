from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import *
from .models import *
from .filters import *
from .serializer import *
# Create your views here.

@csrf_exempt
@permission_classes([IsAuthenticated])
def requests(request):
    match request.method:
        case "POST":
            if request.user.role == "USER":
                form = UserRequestForm(request.POST, request.FILES)
                if not form.is_valid():
                    return render(request, 'create_request.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
            else:
                form = RequestForm(request.POST, request.FILES)
                if not form.is_valid():
                    return render(request, 'create_request.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)
                instance = form.save()
            return redirect(f'/requests/{instance.id}/')
        case "GET":
            form = RequestForm()
            if request.user.role == "USER":
                form = UserRequestForm()
            return render(request, 'create_request.html', {'form': form})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_requests(request):
    filter = RequestFilter(request.GET, queryset=Request.objects.all())
    if request.user.role == "USER":
        filter = RequestFilter(request.GET, queryset=Request.objects.filter(user_id = request.user.id))    
    return render(request, 'get_all.html', {'requests': filter.qs})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_request(request, pk):
    obj = Request.objects.prefetch_related("request_comments").get(pk=pk)
    if request.user.role == "USER":
        if obj.user != request.user:
            return HttpResponse("Forbidden", status=status.HTTP_403_FORBIDDEN)
    return render(request, 'get.html', {
        'request': Request.objects.prefetch_related("request_comments").get(pk=pk),
        'form': RequestCommentForm()
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request_comment_form(request, id):
    if request.user.role == "USER":
        return HttpResponse("Forbidden", status=status.HTTP_403_FORBIDDEN)
    
    if request.method != 'POST':          
        return render(request, 'create_request_comment.html', {'form': RequestCommentForm()})
    
    form = RequestCommentForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_request_comment.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

    instance = form.save(commit=False)
    instance.request_id = id
    instance.user = request.user
    instance.save()
    return HttpResponse(instance.id, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def api_request(request, pk):
    match request.method:
        case "PATCH":
            if request.user.role == "USER":    
                return HttpResponse("Forbidden", status=status.HTTP_403_FORBIDDEN)
            
            instance = Request.objects.get(pk=pk)
            serializer = RequestPatchSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            
            return Response(instance.id, status=status.HTTP_200_OK)
        case "DELETE":
            if request.user.role != "ADMIN":
                return HttpResponse("Forbidden", status=status.HTTP_403_FORBIDDEN)
            
            Request.objects.get(pk=pk).delete()
            return Response("Deleted")
