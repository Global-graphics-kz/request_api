from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from .forms import *
from .models import *
from .filters import *
from .serializer import *
# Create your views here.

def requests(request):
    match request.method:
        case "POST":
            form = RequestForm(request.POST, request.FILES)
            if not form.is_valid():
                return render(request, 'create_request.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)

            instance = form.save()
            return redirect(f'/requests/requests/{instance.id}/')
        case "GET":
            return render(request, 'create_request.html', {'form': RequestForm()})

api_view(['GET'])
def get_requests(request):
    filter = RequestFilter(request.GET, queryset=Request.objects.all())
    return render(request, 'get_all.html', {'requests': filter.qs})

api_view(['GET'])
def get_request(request, pk):
    return render(request, 'get.html', {
        'request': Request.objects.prefetch_related("request_comments").get(pk=pk),
        'form': RequestCommentForm()
    })

api_view(['POST'])
def create_request_comment_form(request, id):
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

@api_view(["PATCH", "DELETE"])
def api_request(request, pk):
    match request.method:
        case "PATCH":
            instance = Request.objects.get(pk=pk)
            serializer = RequestPatchSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            
            return Response(instance.id, status=status.HTTP_200_OK)
        case "DELETE":
            Request.objects.get(pk=pk).delete()
            return Response("Deleted")
