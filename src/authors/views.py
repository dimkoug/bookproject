from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings

from books.models import BookAuthor

from core.functions import is_ajax
from core.mixins import *
from core.views import *
from .forms import *


class AuthorListView(BaseListView):

    model = Author
    queryset = Author.objects.select_related('profile').prefetch_related(Prefetch('bookauthors',queryset=BookAuthor.objects.select_related('book'),to_attr='books'))
    paginate_by = settings.PAGINATED_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
    
    
class AuthorDetailView(BaseDetailView):
    model = Author

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
    
class AuthorCreateView(BaseCreateView):
    model = Author
    form_class = AuthorForm


    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)



class AuthorUpdateView(BaseUpdateView):
    model = Author
    form_class = AuthorForm




class AuthorDeleteView(BaseDeleteView):
    model = Author
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset