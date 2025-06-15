from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from authors.models import Author
from core.forms import BootstrapForm

from publishers.models import Publisher
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
        
        category_queryset = Category.objects.select_related('profile').filter(profile_id=self.request.user.profile.id)
        publisher_queryset = Publisher.objects.select_related('profile').filter(profile_id=self.request.user.profile.id)
      

            
            
        if self.instance.pk:
            category_queryset = Category.objects.select_related('profile').filter(profile_id=self.request.user.profile.id,id=self.instance.category_id)
            publisher_queryset = Publisher.objects.select_related('profile').filter(profile_id=self.request.user.profile.id,id=self.instance.publisher__id)

        
        
        
        self.fields['category'].queryset = category_queryset
        self.fields['category'].widget.queryset = category_queryset
        self.fields['publisher'].queryset = publisher_queryset
        self.fields['publisher'].widget.queryset = publisher_queryset


class FilteredBookAuthorForm(forms.ModelForm):
    class Meta:
        model = BookAuthor
        fields = ('author',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # safer with default None
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['author'].queryset = Author.objects.select_related('profile').filter(
                profile_id=self.request.user.profile.id
            )


class BookAuthorBaseFormSet(BootstrapFormSet,BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['request'] = self.request
        return super()._construct_form(i, **kwargs)



BookFormSet = inlineformset_factory(Category, Book, BookForm, formset=unique_bootstrap_field_formset('name'), can_delete=True)
BookAuthorFormSet = inlineformset_factory(Book, BookAuthor, form=FilteredBookAuthorForm,formset=BookAuthorBaseFormSet, can_delete=True)
