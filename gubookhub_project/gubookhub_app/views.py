from django.shortcuts import render
from gubookhub_app.forms import UserForm, ProfileForm, BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from gubookhub_app.google_books_api import run_query
from gubookhub_app.models import Subject, Course, Book, User, Profile, Favorite
from gubookhub_app.helpers import list_courses, list_subjects, list_split
from django.contrib import messages
from django.views.generic.base import View
from django.conf import settings
from django.utils.decorators import method_decorator


# Create your views here.

def index(request):
    return render(request, 'gubookhub/index.html')


def about(request):
    return render(request, 'gubookhub/about.html')


def profile_page(request, username):
    context_dict = {}
    # get the user object using the username from the URL
    user = User.objects.get(username=username)

    context_dict['username'] = user.username
    context_dict['email'] = user.email
    if hasattr(user, 'profile'):
        context_dict['profile'] = user.profile
    # get the books uploaded by the user
    context_dict['books'] = Book.objects.filter(user=user)

    # get the books favourited by the user
    favourite_books = Favorite.objects.filter(user=user)
    context_dict['favourites'] = favourite_books

    return render(request, 'gubookhub/profile_page.html', context=context_dict)


def search(request):
    # set default query to an empty string
    query = ''
    # where data from Google will be stored
    results = []
    context_dict = {}

    # request data from the API only then a POST request is issued
    if request.method == "POST":
        query = request.POST["query"].strip()

        if query:
            api_response = run_query(query)
            for item in api_response:
                results.append(item['volumeInfo'])
            context_dict['results'] = results
            # keep the query in the page
            context_dict['query'] = query

    return render(request, 'gubookhub/search.html', context=context_dict)


def subject(request, subject_name_slug):
    subject = Subject.objects.get(slug=subject_name_slug)
    associated_courses = Course.objects.filter(subject=subject)
    context = {'subject': subject, 'courses': associated_courses, }
    return render(request, 'gubookhub/subject.html', context=context)


def course(request, subject_name_slug, course_title):
    course = Course.objects.get(title=course_title)
    book_list = Book.objects.filter(course=course).order_by('title')
    subject = Subject.objects.get(slug=subject_name_slug)
    context = {'course': course, 'books': book_list, 'subject': subject}
    return render(request, 'gubookhub/course.html', context=context)


@login_required
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # save the object but not in the database, yet.
            book = form.save(commit=False)
            book.user = request.user
            # after retrieving the user, add it as attribute and save changes in database
            book.save()
            messages.success(request, 'Book successfully added.')
            return redirect('/gubookhub_app/')
        else:
            print(form.errors)
    return render(request, 'gubookhub/add_book.html', {'form': form})


@login_required
def edit_profile(request):
    context_dict = {}
    # flag used by template so let the user know the changes have been made
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


# class will be used as a view for asynchronous data retrieval
class CourseListingView(View):
    def get(self, request):
        if "suggestion" in request.GET:
            suggestion = request.GET["suggestion"]
            subject = request.GET["subject"]
        else:
            # default suggestion if not suggestion found in the request
            suggestion = ""

        course_list = list_courses(subject_name=subject, contains=suggestion)
        # if no data is found using the query, retrieve everything from the database
        if len(course_list) == 0:
            subject_obj = Subject.objects.get(name=subject)
            course_list = Course.objects.filter(subject=subject_obj).order_by('title')
        context = {}
        context['courses'] = course_list
        # dictionary to keep track the number of books for each course to display on the page
        number_of_books = {}
        for course in course_list:
            number_of_books[course] = len(Book.objects.filter(course=course))
        context['number_of_books'] = number_of_books

        return render(request, 'gubookhub/courses.html', context=context)


class SubjectListingView(View):
    def get(self, request):
        if "suggestion" in request.GET:
            suggestion = request.GET["suggestion"]
        else:
            suggestion = ""

        subjects_list = list_subjects(contains=suggestion)
        if len(subjects_list) == 0:
            subjects_list = Subject.objects.all().order_by('name')

        # split the subjects list into multiple lists, 6 elements each.
        # this property allows Bootstrap to function properly when using columns
        subjects_output = list_split(subjects_list, 6)

        return render(request, 'gubookhub/subjects_card.html', {'subjects_output': subjects_output})


class FavouriteBookView(View):
    @method_decorator(login_required)
    def get(self, request):
        book_id = request.GET['book_id']
        user_obj = User.objects.get(username=request.user)
        try:
            book = Book.objects.get(id=int(book_id))
            # if an object is found, 'access' will be 'false'
            favourite, access = Favorite.objects.get_or_create(user=user_obj, book=book)
        except Book.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        if access:
            book.favorite_count = len(Favorite.objects.filter(book=book))
            book.save()
        else:
            # -2 signifies if the favourite already exists or not
            return HttpResponse(-2)

        return HttpResponse(book.favorite_count)


class SubjectMoreInfoView(View):
    def get(self, request):
        subject = request.GET['subject']
        subj_obj = Subject.objects.get(slug=subject)

        courses = Course.objects.filter(subject=subj_obj)
        number_of_courses = len(courses)

        # get books which their course is in the courses list
        books = Book.objects.filter(course__in=courses)
        number_of_books = len(books)

        favs = Favorite.objects.filter(book__in=books)
        number_of_favs = len(favs)
        # return a json response
        return JsonResponse({
            'number_of_courses': number_of_courses,
            'number_of_books': number_of_books,
            'number_of_favs': number_of_favs
        })
