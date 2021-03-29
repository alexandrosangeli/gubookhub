from django import template
from gubookhub_app.models import Course, Subject

register = template.Library()

@register.inclusion_tag('gubookhub/courses.html')
def get_courses_list(subject_name):
    subject = Subject.objects.get(name=subject_name)
    return {'courses': Course.objects.filter(subject=subject).order_by('title')}