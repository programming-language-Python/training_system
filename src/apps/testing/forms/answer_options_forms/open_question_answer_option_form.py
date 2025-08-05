from django import forms

from apps.testing.models.task_answer_options import OpenQuestionAnswerOption


class OpenQuestionAnswerOptionForm(forms.ModelForm):
    class Meta:
        model = OpenQuestionAnswerOption
        widgets = {
            'correct_answer': forms.TextInput(attrs={
                'class': 'uk-input uk-form-width-small uk-form-small'
            })
        }
        fields = ('correct_answer',)
