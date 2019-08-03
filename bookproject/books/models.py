from django.db import models
from django.utils.html import format_html, mark_safe

class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Timestamped):
    name = models.CharField(max_length=100)

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Author(Timestamped):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='authors/', null=True, blank=True)

    class Meta:
        default_related_name = 'authors'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''




class Book(Timestamped):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    image = models.ImageField(upload_to='covers/', null=True, blank=True)

    class Meta:
        default_related_name = 'books'
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.name

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''


class BookAuthor(Timestamped):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bookauthors'
        verbose_name = 'book author'
        verbose_name_plural = 'book authors'

    def __str__(self):
        return self.author.name
