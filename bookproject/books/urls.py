from django.urls import path

from . import views

from .functions import (
    get_sb_authors_data,
    get_sb_categories_data
)


app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('add/', views.BookCreateView.as_view(), name='book-create'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name='author-delete'),

    path('get_sb_authors_data/', get_sb_authors_data, name='sb-authors'),
    path('get_sb_categories_data/', get_sb_categories_data, name='sb-categories'),

]
