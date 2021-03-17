import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gubookhub_project.settings',)

import django
django.setup()

from gubookhub_app.models import Subject, Course, Book

def populate():

    eng_courses = [
        {'title' : 'ENG1003', 'level' : 1},
        {'title' : 'ENG3035', 'level' : 3},
    ]

    cs_courses = [
        {'title' : 'COMPSCI1001', 'level' : 1},
        {'title' : 'COMPSCI2004', 'level' : 2},
        {'title' : 'COMPSCI4014', 'level' : 3},
    ]

    subjects = {
        'Computing Science' : {'courses' : cs_courses},
        'Mechanical Engineering' : {'courses' : eng_courses},
    }

    for subject, subject_data in subjects.items():
        s = add_subject(subject)
        for course in subject_data['courses']:
            add_course(s, course['title'], course['level'])

    for s in Subject.objects.all():
        for c in Course.objects.filter(subject=s):
            print(f'- {s}: {c}')

def add_subject(name):
    subject = Subject.objects.get_or_create(name=name)[0]
    subject.save()
    return subject

def add_course(subject, title, level):
    course = Course.objects.get_or_create(subject=subject, title=title, level=level)[0]
    #course.level = level
    course.subject = subject
    course.save()
    return course

if __name__ == '__main__':
    print("Starting to populate...")
    populate()
    print("Done.")