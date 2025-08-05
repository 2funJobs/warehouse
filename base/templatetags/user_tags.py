from django import template

register = template.Library()

@register.simple_tag
def is_superuser(user):
    return user.is_authenticated and user.is_superuser
