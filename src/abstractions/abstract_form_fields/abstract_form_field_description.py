from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class AbstractFormFieldDescription(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        widget=CKEditorUploadingWidget()
    )
