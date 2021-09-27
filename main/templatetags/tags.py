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
    try:
        return models.Week.get_files(week_id)
    except:
        return []

@register.filter
def is_available(sub, week_no):
    if week_no<=sub.progress.week_no:
        
        return True
    else:
        
        return False

@register.filter
def get_percentage(sub):
    try:
        val = sub.progress.week_no/sub.total_weeks*100
        return str(round(val, 2))
    except:
        return 0

@register.filter
def quiz_available(sub, week_no):
    
    if sub.quiz_approve or sub.progress.week_no > week_no:
        print("true")
        return True
    else:
        print("false")
        return False

@register.simple_tag
def check_subscription(course, user):
    if course.check_subscription(user):
        return True
    return False