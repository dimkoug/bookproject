from django.db import models
from django.utils.html import format_html, mark_safe


from core.models import Timestamped

class Category(Timestamped):
    name = models.CharField(max_length=100)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Book(Timestamped):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    publisher = models.ForeignKey('publishers.Publisher', on_delete=models.CASCADE)
    authors = models.ManyToManyField('authors.Author', through='BookAuthor', symmetrical=False, blank=True)
    image = models.ImageField(upload_to='covers/', null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    language = models.CharField(max_length=50)
    pages = models.PositiveIntegerField()

    genre = models.CharField(max_length=100)
    format = models.CharField(max_length=50, choices=[('Paperback', 'Paperback'), ('Hardcover', 'Hardcover'), ('eBook', 'eBook')])
    edition = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(blank=True)

    copies_available = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, blank=True)  # e.g., "Shelf A3"
    is_available = models.BooleanField(default=True)

    dewey_decimal = models.CharField(max_length=20, blank=True, null=True)
    library_of_congress = models.CharField(max_length=20, blank=True, null=True)

    file_url = models.URLField(blank=True, null=True)
    file_format = models.CharField(max_length=10, blank=True, null=True)
    

    class Meta:
        default_related_name = 'books'
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''


class BookAuthor(Timestamped):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bookauthors'
        verbose_name = 'book author'
        verbose_name_plural = 'book authors'
