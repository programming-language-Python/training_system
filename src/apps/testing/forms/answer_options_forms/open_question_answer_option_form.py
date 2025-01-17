from django import forms

from apps.testing.models.task_answer_options import OpenQuestionAnswerOption


class OpenQuestionAnswerOptionForm(forms.ModelForm):
    class Meta:
        model = OpenQuestionAnswerOption
        fields = ('correct_answer',)
