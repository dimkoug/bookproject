from django.urls import path

from core.patterns import get_patterns

from .functions import (
    get_sb_authors_data,
    get_sb_categories_data
)


app_name = 'books'

urlpatterns = get_patterns(app_name,'views') + [
    path('get_sb_authors_data/', get_sb_authors_data, name='sb-authors'),
    path('get_sb_categories_data/', get_sb_categories_data, name='sb-categories'),

]
