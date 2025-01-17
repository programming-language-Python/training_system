from django import forms

from apps.testing.models import SolvingTask


class SolvingTaskForm(forms.ModelForm):
    class Meta:
        model = SolvingTask
        fields = ('answer',)
