from django.core.exceptions import ValidationError


def clean_email(value):
    email = value
    if '.edu' in email:
        raise ValidationError('We do not accept edu emails')


CATEGORIES = ['Mexican', 'Asian', 'American' 'Whatever']


def validate_category(value):
    upp = value.capitalize()
    if upp not in CATEGORIES:
        raise ValidationError('{} not in category'.format(value))
