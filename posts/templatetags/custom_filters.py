from django import template

register = template.Library()

@register.filter
def get_genre_name(genre_dict, genre_id):
    return genre_dict.get(genre_id, '')