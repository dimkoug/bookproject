from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from books.models import Category, Author, Book, BookAuthor
from books.forms import CategoryForm, AuthorForm, BookForm


class AuthorListView(ListView):
    model = Author
    queryset = Author.objects.prefetch_related('books')


class AuthorDetailView(DetailView):
    model = Author
    queryset = Author.objects.prefetch_related('books')


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('books:author-list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was created successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                    reverse_lazy('books:author-update',
                                 kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('books:author-list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was updated successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy(
                'books:author-update', kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('books:author-list')


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.prefetch_related('books')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('books:category-list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was created successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy(
                'books:category-update', kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('books:category-list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was updated successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy(
                'books:category-update', kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('books:category-list')


class BookListView(ListView):
    model = Book
    queryset = Book.objects.select_related('category').prefetch_related(Prefetch(
            'bookauthors',
            queryset=BookAuthor.objects.select_related(
                'author',
                'book'
            ),
        ),)


class BookDetailView(DetailView):
    model = Book
    queryset = Book.objects.select_related('category').prefetch_related(Prefetch(
            'bookauthors',
            queryset=BookAuthor.objects.select_related(
                'author',
                'book'
            ),
        ),)


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book-list')

    def get_initial(self):
        initial = super().get_initial()
        if 'category' in self.request.GET:
            initial.update({
                'category': self.request.GET.get('category')
            })
        if 'author' in self.request.GET:
            initial.update({
                'authors': self.request.GET.get('author')
            })
        return initial

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was created successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy(
                'books:book-update', kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book-list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was updated successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(reverse_lazy(
                'books:book-update', kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books:book-list')
