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

def show_course(request, course_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        books = Book.objects.filter(course=course)
        context_dict['course'] = course
        context_dict['books'] = books
    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['books'] = None

    return render(request, 'gubookhub/course.html', context=context_dict)

def show_subject(request, subject_name_slug):
    context_dict = {}

    try:
        subject = Subject.objects.get(slug=subject_name_slug)
        courses = Course.objects.filter(subject=subject)
        context_dict['subject'] = subject
        context_dict['courses'] = courses
    except Subject.DoesNotExist:
        context_dict['subject'] = None
        context_dict['courses'] = None

    return render(request, 'gubookhub/subject.html', context=context_dict)

@login_required
def add_book(request, course_name_slug):
    try:
        course = Course.objects.get(slug=course_name_slug)
    except:
        course = None

    if course is None:
        return redirect(reverse('gubookhub_app:index'))

    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            if course:
                book = form.save(commit=False)
                book.course = course
                book.save()

                return redirect(reverse('gubookhub_app:show_course', kwargs={'course_name_slug': course_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'gubookhub/add_book.html', context=context_dict)