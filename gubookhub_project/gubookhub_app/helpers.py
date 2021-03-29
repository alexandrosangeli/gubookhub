from gubookhub_app.models import Course, Subject


def list_courses(subject_name, max_results=0, contains=""):
    course_list = []
    subject = Subject.objects.get(name=subject_name)
    if contains:
        course_list = Course.objects.filter(subject=subject, title__icontains=contains).order_by('title')

    if max_results > 0:
        if len(course_list) > max_results:
            course_list = course_list[:max_results]

    return course_list