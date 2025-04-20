from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from core.forms import BootstrapForm

from .models import *

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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class BookForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'category','publisher','isbn','publication_date','language','pages','genre','format',
                  'edition','summary','copies_available','location','is_available',
                  'dewey_decimal','library_of_congress','file_url','file_format',
                  'image')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)



BookFormSet = inlineformset_factory(Category, Book, BookForm, formset=unique_bootstrap_field_formset('name'), can_delete=True)
BookAuthorFormSet = inlineformset_factory(Book, BookAuthor, fields=('author',),formset=unique_bootstrap_field_formset('author'), can_delete=True)
