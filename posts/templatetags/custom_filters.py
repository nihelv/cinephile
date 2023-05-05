from django import template
from posts.models import genre_dict

register = template.Library()

@register.filter
def get_genre_name(genre_dict, genre_id):
    return genre_dict.get(genre_id, '')