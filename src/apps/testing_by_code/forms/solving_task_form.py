from django import forms

from apps.testing_by_code.models import SolvingTask


class SolvingTaskForm(forms.ModelForm):
    answer = forms.CharField(
        label='Ответ',
        required=False,
        widget=forms.TextInput()
    )

    class Meta:
        model = SolvingTask
        fields = ('answer',)
