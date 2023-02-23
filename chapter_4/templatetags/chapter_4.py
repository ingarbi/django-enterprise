from django.template import Library

register = Library()


@register.filter(name='vehicle_make')
def vehicle_make(value):
    from chapter_3.models import MAKE_CHOICES
    for i, choice in enumerate(MAKE_CHOICES):
        if i == value:
            try:
                return choice[1]
            except ValueError:
                pass
    return ''
