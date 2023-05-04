from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_genre_name(genre_dict, genre_id):
    return genre_dict.get(genre_id, '')


@register.filter
def convert_str_date(value):
    return datetime.strptime(value, '%Y-%m-%d')