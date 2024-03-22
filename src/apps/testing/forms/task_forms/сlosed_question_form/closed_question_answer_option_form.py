from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.testing.models.tasks.closed_question import ClosedQuestionAnswerOption


class ClosedQuestionAnswerOptionForm(forms.ModelForm):
    answer_option_meta = ClosedQuestionAnswerOption._meta
    serial_number = forms.IntegerField(
        label=answer_option_meta.get_field('serial_number').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': 'serial-number',
                'data-name': 'serial-number',
                'min': 1
            }
        )
    )
    description = forms.CharField(
        label=answer_option_meta.get_field('description').verbose_name,
        widget=CKEditor5Widget(
            attrs={
                'class': 'django_ckeditor_5',
                'data-name': 'description'
            }
        )
    )
    is_correct = forms.BooleanField(
        label=answer_option_meta.get_field('is_correct').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox',
                'data-name': 'is-correct',
            }
        )
    )

    class Meta:
        model = ClosedQuestionAnswerOption
        fields = ('serial_number', 'description', 'is_correct', 'closed_question',)
