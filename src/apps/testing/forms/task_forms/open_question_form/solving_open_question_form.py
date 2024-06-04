from django import forms

from apps.testing.models.solving_tasks.solving_open_question import SolvingOpenQuestion


class SolvingOpenQuestionForm(forms.ModelForm):
    class Meta:
        model = SolvingOpenQuestion
        fields = ['answer', ]
