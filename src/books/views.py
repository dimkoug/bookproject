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

from authors.models import Author

from core.functions import is_ajax
from core.mixins import *
from core.views import *
from .forms import *



class BaseListView(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class CategoryDetailView(BaseDetailView):
    model = Category

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class CategoryListView(BaseListView):

    model = Category
    paginate_by = settings.PAGINATED_BY
    queryset = Category.objects.prefetch_related('books')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm


    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)



class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm



class CategoryDeleteView(BaseDeleteView):
    model = Category
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class BookDetailView(BaseDetailView):
    model = Book

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookListView(BaseListView):

    model = Book
    paginate_by = settings.PAGINATED_BY
    query = Book.objects.select_related('category', 'profile').prefetch_related('authors')

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        authors = self.request.GET.getlist('author')
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        if category:
            queryset = queryset.filter(category=category)
        if len(authors) > 0:
            queryset = queryset.filter(authors__in=authors)
        return queryset




class BookCreateView(BaseCreateView):
    model = Book
    form_class = BookForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Authors',
                'formset': BookAuthorFormSet(self.request.POST or None,
                                             queryset=Author.objects.select_related('profile').filter(profile_id=self.request.user.profile)),
                "sb_url": reverse("authors:sb-authors")
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = self.request.user.profile
            obj.save()
            formsets = [
                BookAuthorFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class BookUpdateView(BaseUpdateView):
    model = Book
    form_class = BookForm


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Address',
                'formset': BookAuthorFormSet(
                    self.request.POST or None,instance=self.get_object()),
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            formsets = [
                BookAuthorFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class BookDeleteView(BaseDeleteView):
    model = Book
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
