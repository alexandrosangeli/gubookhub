from django import forms
from django.contrib.auth.models import User
from gubookhub_app.models import Book, Profile, Course
from registration.forms import RegistrationFormUniqueEmail


class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=Book.TITLE_MAX_LENGTH, help_text="Please enter the title of the book.")
    author = forms.CharField(max_length=Book.AUTHOR_MAX_LENGTH, help_text="Please enter the author's name.")
    url = forms.URLField(max_length=Book.URL_MAX_LENGTH, help_text="Optional: Add an associated url.")
    course = forms.URLField(help_text="Please add the associated course.")

    class Meta:
        model = Book
        exclude = ('course',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)  


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('level', 'subject', 'picture',)