from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import fields as django_fields
from gubookhub_app.models import Book, Course
from gubookhub_app.forms import BookForm
from django.contrib.auth.models import User

class UserAuthenticationTests(TestCase):
    pass;

class StructureTests(TestCase):
    pass;

class SearchTests(TestCase):
    pass;

class AddBookTests(TestCase):
    fixtures = ["tests.json", ]
    def test_add_book_functionality(self):
        form = BookForm(data={'title':'Tango with Django 2', 'author':'Leif Azzopardi', "url":"https://moodle.gla.ac.uk/pluginfile.php/3433670/mod_resource/content/1/twd-uog-lib-2021-01-07.pdf", "favorite_count":0, "course":1, "user":User.objects.get(username="vertex")})
        self.assertTrue(form.is_valid(), "Form is invalid.")

class URLTests(TestCase):
    def test_add_book_url_mapping(self):
        try:
            resolved_name = resolve('/gubookhub_app/add_book/').view_name
        except:
            resolved_name = ''

        self.assertEqual(resolved_name, "gubookhub_app:add_book", "The lookup of URL '/gubookhub_app/add_book/' did not return a mapping name of 'gubookhub_app:add_book'.")
