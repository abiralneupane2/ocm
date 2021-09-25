from django import template
from django.http import request
from .. import models
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_course_by_categories(category):
    try:
        return models.Course.get_courses_by_categories(category)
    except:
        return False


@register.filter
def get_course_by_university(university):
    try:
        return models.Course.get_courses_by_university(university)
    except:
        return False

@register.filter
def get_files_url(week_id):
    print(week_id)
    try:
        return models.Week.get_files(week_id)
    except:
        return []

@register.filter
def get_value(week):
    return "value"

@register.filter
def get_percentage(sub):
    try:
        return sub.progress/sub.total_weeks*100
    except:
        return 0
@register.simple_tag
def check_subscription(course, user):
    if course.check_subscription(user):
        return True
    return False