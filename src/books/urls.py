from django.urls import path

from core.patterns import get_patterns

from .functions import (
    get_sb_categories_data
)


app_name = 'books'

urlpatterns = get_patterns(app_name,'views') + [
    path('categories/sb/', get_sb_categories_data, name='sb-categories'),

]
