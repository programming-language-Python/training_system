from django import forms

from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionForm(forms.ModelForm):
    class Meta:
        model = ClosedQuestion
        checkbox_input = forms.CheckboxInput(attrs={
            'class': 'uk-checkbox'
        })
        widgets = {
            'is_several_correct_answers': checkbox_input,
            'is_random_order_answer_options': checkbox_input,
            'is_partially_correct_execution': checkbox_input,
        }
        exclude = ('task',)
