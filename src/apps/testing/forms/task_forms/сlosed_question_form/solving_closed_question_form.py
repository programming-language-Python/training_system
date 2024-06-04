from django import forms

from apps.testing.models.solving_tasks import SolvingClosedQuestion


class SolvingClosedQuestionForm(forms.ModelForm):
    class Meta:
        model = SolvingClosedQuestion
        fields = ['answer', ]
