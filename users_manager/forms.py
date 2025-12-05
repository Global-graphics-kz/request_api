from django import forms
from .models import *

class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "role", "password"]

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def save(self, commit = ...):
        user = super().save(commit=False)
        user.role = "USER"
        if commit:
            user.save()
        return user
    