from django import forms

from apps.testing.models.task_answer_options import OpenQuestionAnswerOption


class OpenQuestionAnswerOptionForm(forms.ModelForm):
    answer_option_meta = OpenQuestionAnswerOption._meta
    correct_answer = forms.CharField(
        label=answer_option_meta.get_field('correct_answer').verbose_name
    )

    class Meta:
        model = OpenQuestionAnswerOption
        fields = ('correct_answer', 'open_question',)
