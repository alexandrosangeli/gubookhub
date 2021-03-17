from django import forms

from django.contrib.auth.models import User
from gubookhub_app.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class meta:
        model = Profile
        fields = ('level', 'subject', 'picture')