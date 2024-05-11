from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class AbstractFormFieldDescription(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        initial='Описание',
        widget=CKEditor5Widget(
            attrs={
                'class': 'form-control django_ckeditor_5',
                'data-name': 'description'
            }
        )
    )
