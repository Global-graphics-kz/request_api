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

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    