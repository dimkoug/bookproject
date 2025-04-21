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



class PublisherForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name','website', 'image')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class PublishingContractForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = PublishingContract
        fields = ('publisher', 'author','contract_date', 'expiry_date')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)