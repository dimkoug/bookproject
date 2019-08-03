from django.urls import path

from books.views import (AuthorListView, AuthorDetailView, AuthorCreateView,
                         AuthorUpdateView, AuthorDeleteView,
                         CategoryListView, CategoryDetailView,
                         CategoryCreateView, CategoryUpdateView,
                         CategoryDeleteView, BookListView, BookDetailView,
                         BookCreateView, BookUpdateView, BookDeleteView
                         )

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),
    path('categories/create/', CategoryCreateView.as_view(),
         name='category-create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(),
         name='category-update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(),
         name='category-delete'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
    path('authors/update/<int:pk>/', AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author-delete'),

]
