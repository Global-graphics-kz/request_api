from django.urls import path
from .views import *

urlpatterns = [
    path('create/', requests),
    path('', get_requests),
    path('<int:pk>/', get_request),
    path('<int:id>/comments', create_request_comment_form),
    path('<int:pk>', api_request),
]