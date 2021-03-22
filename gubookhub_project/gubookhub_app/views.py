from django.shortcuts import render
from gubookhub_app.forms import UserForm, ProfileForm, BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from gubookhub_app.google_books_api import run_query
from gubookhub_app.models import Subject, Course, Book

# Create your views here.

def index(request):
    subject_list = Subject.objects.order_by('name')
    course_list = Course.objects.order_by('title')
    book_list = Book.objects.order_by('title')

    context_dict = {}

    context_dict['boldmessage'] = 'Find resources that are right for you!'
    context_dict['subjects'] = subject_list
    context_dict['courses'] = course_list

    return render(request, 'gubookhub/index.html', context=context_dict)

def about(request):
    context_dict = {}

    context_dict['aboutmessage'] = 'This is a student made resource hub for the University of Glasgow students. It features a collection of useful textbooks and resources submitted by fellow students across various schools from various years.'

    return render(request, 'gubookhub/about.html', context = context_dict)

def search(request):
    results = []

    if request.method == "POST":
        query = request.POST["query"].strip()

        if query:
            api_response = run_query(query)
            for item in api_response:
                results.append(item['volumeInfo'])

    return render(request, 'gubookhub/search.html', context={'results':results})

@login_required
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/gubookhub_app/')
        else:
            print(form.errors)

    return render(request, 'gubookhub/add_book.html', {'form': form})
