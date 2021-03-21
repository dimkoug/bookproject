from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Category, Author,Book, BookAuthor


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


class BootstrapFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for form in self.forms:
            for field in form.fields:
                widget_name = form.fields[field].widget.__class__.__name__
                if widget_name not in fields:
                    form.fields[field].widget.attrs.update({
                        'class': 'form-control'
                    })
    def add_fields(self, form, index):
        super().add_fields(form, index)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in form.fields:
            widget_name = form.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                form.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


def unique_bootstrap_field_formset(field_name):
    class UniqueFieldBootstrapFormSet(BootstrapFormSet):
        def clean(self):
            if any(self.errors):
                # Don't bother validating the formset unless each form is valid on its own
                return
            values = set()
            for form in self.forms:
                if form.cleaned_data:
                    value = form.cleaned_data.get(field_name)
                    if value:
                        if value in values:
                            form[field_name].field.widget.attrs['class'] += ' is-invalid'
                            form.add_error(field_name, "{} {} cannot be added multiple times.".format(
                                field_name, value))
                        values.add(value)
    return UniqueFieldBootstrapFormSet



class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class AuthorForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'image')

class BookForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'category', 'image')

BookFormSet = inlineformset_factory(Category, Book, fields=('name',), formset=unique_bootstrap_field_formset('name'), can_delete=True)
AuthorFormSet = inlineformset_factory(Category, Book, fields=('name',),formset=unique_bootstrap_field_formset('name'), can_delete=True)
BookAuthorFormSet = inlineformset_factory(Book, BookAuthor, fields=('author',),formset=unique_bootstrap_field_formset('author'), can_delete=True)
