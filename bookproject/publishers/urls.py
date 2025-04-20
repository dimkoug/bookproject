from django.urls import path

from core.patterns import get_patterns

from .functions import (
    get_sb_data
)


app_name = 'publishers'

urlpatterns = get_patterns(app_name,'views') + [
    path('sb/', get_sb_data, name='sb-publisher'),

]
