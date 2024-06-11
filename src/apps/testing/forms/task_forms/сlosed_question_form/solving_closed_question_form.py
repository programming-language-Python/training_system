from django import forms

from apps.testing.models.solving_tasks import SolvingClosedQuestion


class SolvingClosedQuestionForm(forms.ModelForm):
    answer = forms.MultipleChoiceField(
        label='Варианты ответов',
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = SolvingClosedQuestion
        fields = ['answer', ]
