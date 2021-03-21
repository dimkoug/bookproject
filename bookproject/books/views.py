from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
from .models import Category, Author,Book
from .forms import CategoryForm, AuthorForm,BookForm, BookFormSet, BookAuthorFormSet


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorListView(ListView):

    model = Author
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('books:author-list')


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('books:author-list')


class AuthorDeleteView(DeleteView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('books:author-list')


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):

    model = Category
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('books:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BookFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            formset = BookFormSet(self.request.POST, instance=obj)
            if formset.is_valid():
                formset.save()
        return super().form_valid(form)



class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('books:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BookFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            formset = BookFormSet(self.request.POST, instance=self.get_object())
            if formset.is_valid():
                formset.save()
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('books:category-list')


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookListView(ListView):

    model = Book
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BookAuthorFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            formset = BookAuthorFormSet(self.request.POST, instance=obj)
            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)
                return super().form_invalid(form)
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BookAuthorFormSet(self.request.POST or None, instance=self.get_object())
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            formset = BookAuthorFormSet(self.request.POST, instance=obj)
            if formset.is_valid():
                formset.save()
                for form_item in formset.deleted_forms:
                    author = form_item.cleaned_data.get('author')
                    if author:
                        author_obj = Author.objects.get(pk=author.pk)
                        obj.authors.remove(author_obj)
            else:
                print(formset.non_form_errors())
                print("formset errors:", formset.errors)
                return super().form_invalid(form)
        return super().form_valid(form)


class BookDeleteView(DeleteView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book-list')
