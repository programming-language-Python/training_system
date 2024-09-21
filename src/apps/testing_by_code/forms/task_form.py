from django import forms

from apps.testing_by_code.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'uk-input uk-form-width-small uk-form-small',
                'min': 1,
                'value': 1
            })
        }
        fields = ('weight',)
