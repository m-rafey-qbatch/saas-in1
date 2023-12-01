from django import template
from socialmedia.models import Submission

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_assignment_for_unit(assignments, unit):
    return next((a for a in assignments if a.unit == unit), None)


@register.filter(name='key')
def key(d, key_name):
    return d[key_name]


@register.filter(name='has_user_submitted')
def has_user_submitted(assignment, user):
    return Submission.objects.filter(assignment=assignment, user=user).exists()


@register.filter(name='get_submission')
def get_submission(value, arg):
    return value.get(arg)