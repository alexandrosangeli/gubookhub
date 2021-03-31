from django.shortcuts import render
from gubookhub_app.forms import UserForm, ProfileForm, BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from gubookhub_app.google_books_api import run_query
from gubookhub_app.models import Subject, Course, Book, User, Profile
from gubookhub_app.helpers import list_courses, list_subjects, list_split
from django.contrib import messages
from django.views.generic.base import View
from django.conf import settings


# Create your views here.

def index(request):
    subject_list = Subject.objects.order_by('name')[:10]
    course_list = Course.objects.order_by('level')[:10]
    book_list = Book.objects.order_by('title')

    context_dict = {}

    context_dict['boldmessage'] = 'Find resources that are right for you!'
    context_dict['subjects'] = subject_list
    context_dict['courses'] = course_list

    return render(request, 'gubookhub/index.html', context=context_dict)

def about(request):
    context_dict = {}

    context_dict['aboutmessage'] = "This is a student made resource hub for the University of Glasgow students. It features a collection of useful textbooks and resources submitted by fellow students across various schools from various years."

    return render(request, 'gubookhub/about.html', context = context_dict)

def search(request):
    query = ''
    results = []
    context_dict = {}

    if request.method == "POST":
        query = request.POST["query"].strip()

        if query:
            api_response = run_query(query)
            for item in api_response:
                results.append(item['volumeInfo'])

            context_dict['results'] = results
            context_dict['query'] = query

    return render(request, 'gubookhub/search.html', context=context_dict)

def subject(request, subject_name_slug):

    subject= Subject.objects.get(slug=subject_name_slug)
    associated_courses = Course.objects.filter(subject=subject)
    context= {'subject':subject, 'courses':associated_courses,}
    
    return render(request, 'gubookhub/subject.html', context=context)

def course(request, subject_name_slug, course_title):

    course = Course.objects.get(title=course_title)
    book_list = Book.objects.filter(course=course).order_by('title')
    subject = Subject.objects.get(slug=subject_name_slug)
    context = {'course':course, 'books':book_list, 'subject':subject}

    return render(request, 'gubookhub/course.html', context=context)


@login_required
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, 'Book successfully added.')
            return redirect('/gubookhub_app/')
        else:
            print(form.errors)

    return render(request, 'gubookhub/add_book.html' ,{'form': form})

@login_required
def edit_profile(request):
    context_dict = {}
    completed = False

    if request.method == 'POST':
        try:
            form = ProfileForm(request.POST, instance=request.user.profile)
        except User.profile.RelatedObjectDoesNotExist:
            form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.user = request.user
            profile.save()
            completed = True
            return HttpResponseRedirect(reverse('gubookhub_app:index'))
        else:
            print(form.errors)
    else:
        form = ProfileForm()

    context_dict['form'] = form
    context_dict['completed'] = completed
    context_dict['username'] = request.user.username
    context_dict['email'] = request.user.email

    if hasattr(request.user, 'profile'):
        context_dict['profile'] = request.user.profile
   
    return render(request, 'gubookhub/edit_profile.html', context_dict)

class CourseListingView(View):
    def get(self, request):
        if "suggestion" in request.GET:
            suggestion = request.GET["suggestion"]
            subject = request.GET["subject"]
        else:
            suggestion = ""

        course_list = list_courses(subject_name=subject, max_results=25, contains=suggestion)
        if len(course_list) == 0:
            subject_obj = Subject.objects.get(name=subject)
            course_list = Course.objects.filter(subject=subject_obj).order_by('title')

        return render(request, 'gubookhub/courses.html', {'courses': course_list})

class SubjectListingView(View):
    def get(self, request):
        if "suggestion" in request.GET:
            suggestion = request.GET["suggestion"]
        else:
            suggestion = ""

        subjects_list = list_subjects(contains=suggestion)
        if len(subjects_list) == 0:
            subjects_list = Subject.objects.all().order_by('name')

        print("hi")
        subjects_output = list_split(subjects_list,6)
        print(subjects_output)

        return render(request, 'gubookhub/subjects_card.html', {'subjects_output': subjects_output})
