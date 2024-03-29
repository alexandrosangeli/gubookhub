import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gubookhub_project.settings',)

import django
django.setup()

from gubookhub_app.models import Subject, Course, Book

# finds the level of a course by getting the first number found in its name
def level(title):
    for elt in title:
        try:
            elt = int(elt)
            return elt
        except Exception:
            continue

def populate():
    #read the subjects from the 'subjects' text file
    with open("population_data/subjects", "r") as sf:
        subject_list = sf.readlines()
        for subject in subject_list:
            subject = subject.strip()
            s = add_subject(subject)
            # read the courses for the subject from the equivalent subject's text file
            with open("population_data/"+subject, "r") as cf:
                course_list = cf.readline().split(" ")
                for course in course_list:
                    add_course(s, course, level(course))

    # show the user what has been added
    for s in Subject.objects.all():
        for c in Course.objects.filter(subject=s):
            print(f'- {s}: {c}')

def add_subject(name):
    subject = Subject.objects.get_or_create(name=name)[0]
    subject.save()
    return subject

def add_course(subject, title, level):
    course = Course.objects.get_or_create(subject=subject, title=title, level=level)[0]
    course.subject = subject
    course.save()
    return course

if __name__ == '__main__':
    # if there is existing data remove it to avoid constaint errors (e.g. subject name must be unique)
    if Subject.objects.all() or Course.objects.all():
        print("Removing existing data...")
        Subject.objects.all().delete()
        Course.objects.all().delete()
        print("Done.")

    print("Starting to populate...")
    populate()
    print("Done.")
