from django import forms

from books.models import Category, Author, Book

class BootstrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class AuthorForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)


class BookForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('category', 'authors', 'name',)
