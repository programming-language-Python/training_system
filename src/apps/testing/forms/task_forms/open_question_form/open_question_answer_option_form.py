from django import forms

from apps.testing.models.tasks.open_question import OpenQuestionAnswerOption


class OpenQuestionAnswerOptionForm(forms.ModelForm):
    answer_option_meta = OpenQuestionAnswerOption._meta
    correct_answer = forms.CharField(
        label=answer_option_meta.get_field('correct_answer').verbose_name
    )

    class Meta:
        model = OpenQuestionAnswerOption
        fields = ('correct_answer', 'open_question',)
