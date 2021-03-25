from django import template
from gubookhub_app.models import Course

register = template.Library()

@register.inclusion_tag('gubookhub/courses.html')
def get_courses_list(num):
    return {'courses': Course.objects.order_by('level')[:num]}