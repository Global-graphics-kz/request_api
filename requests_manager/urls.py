from django.urls import path
from .views import *

urlpatterns = [
    path('requests/create/', requests),
    path('requests/', get_requests),
    path('requests/<int:pk>/', get_request),
    path('requests/<int:id>/comments', create_request_comment_form),
    path('requests/<int:pk>', api_request),
]