from gubookhub_app.models import Course


def list_courses(max_results=0, starts_with=""):
    course_list = []

    if starts_with:
        course_list = Course.objects.filter(title__istartswith=starts_with)

    if max_results > 0:
        if len(course_list) > max_results:
            course_list = course_list[:max_results]

    return course_list