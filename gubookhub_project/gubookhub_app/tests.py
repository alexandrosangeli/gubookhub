import os
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import fields as django_fields
from django.conf import settings
from gubookhub_app.models import Book, Course
from gubookhub_app import forms
from django.contrib.auth.models import User

class UserAuthenticationTests(TestCase):
     def test_user_form(self):
        self.assertTrue('UserForm' in dir(forms), "UserForm is not present in forms.py.")

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, "User form does not match with user model.")

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.")

class StructureTests(TestCase):
    def test_base_template_exists(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'gubookhub', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), "Base template does not exist.")

class SearchTests(TestCase):
    pass;

class AddBookTests(TestCase):
    fixtures = ["tests.json", ]
    def test_add_book_functionality(self):
        form = forms.BookForm(data={'title':'Tango with Django 2', 'author':'Leif Azzopardi', "url":"https://moodle.gla.ac.uk/pluginfile.php/3433670/mod_resource/content/1/twd-uog-lib-2021-01-07.pdf", "favorite_count":0, "course":1, "user":User.objects.get(username="vertex")})
        self.assertTrue(form.is_valid(), "Form is invalid.")

class URLTests(TestCase):
    def test_add_book_url_mapping(self):
        try:
            resolved_name = resolve('/gubookhub_app/add_book/').view_name
        except:
            resolved_name = ''

        self.assertEqual(resolved_name, "gubookhub_app:add_book", "The lookup of URL '/gubookhub_app/add_book/' did not return a mapping name of 'gubookhub_app:add_book'.")
