from django import forms
from .models import *

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["user", "status", "priority", "file"]

class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ["content"]
