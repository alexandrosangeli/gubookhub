from django import template
from gubookhub_app.models import Course, Subject, Book
from gubookhub_app.helpers import list_split


register = template.Library()

# retrieved all the courses under a subject from a database
@register.inclusion_tag('gubookhub/courses.html')
def get_courses_list(subject_name):
    subject = Subject.objects.get(name=subject_name)
    course_list = Course.objects.filter(subject=subject).order_by('title')
    context = {}
    context['courses'] = course_list
    number_of_books = {}
    for course in course_list:
        number_of_books[course] = len(Book.objects.filter(course=course))
    
    context['number_of_books'] = number_of_books

    return context

#retrieves subjects and rendered by subjects_list which shows subjects as a list (used by the sidebar)
@register.inclusion_tag('gubookhub/subjects_list.html')
def get_subjects_list(current_subject=None):
    return {'subjects' : Subject.objects.all(), 'current_subject':current_subject}

#retrieves subjects and rendered by subjects_card which shows subjects as cards (used by the index page main body)
@register.inclusion_tag('gubookhub/subjects_card.html')
def get_subjects_cards():
    return {'subjects_output' : list_split(Subject.objects.all(),6)}


# custom tag to get a value of a dictionary using a key
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

