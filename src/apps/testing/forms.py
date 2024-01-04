from django import forms

from abstractions.abstract_forms import AbstractTestingForm
from apps.testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD
from apps.testing.models import Testing


class TestingForm(AbstractTestingForm):
    CLASS = 'uk-margin uk-input uk-form-width-medium'
    testing_meta = Testing._meta
    number = forms.IntegerField(
        label=testing_meta.get_field('number').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
            }
        )
    )
    likelihood_guessing_answers = forms.FloatField(
        label=testing_meta.get_field('likelihood_guessing_answers').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
                'max': MIN_ASSESSMENT_THRESHOLD,
                'min': 0,
                'step': '0.01'
            }
        )
    )
    assessment_threshold = forms.IntegerField(
        label=testing_meta.get_field('assessment_threshold').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
                'min': MIN_ASSESSMENT_THRESHOLD,
                'max': MAX_ASSESSMENT_THRESHOLD,
            }
        )
    )
    is_established_order_tasks = forms.BooleanField(
        label=testing_meta.get_field('is_established_order_tasks').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    task_lead_time = forms.TimeField(
        label=testing_meta.get_field('task_lead_time').verbose_name,
        widget=forms.TimeInput(
            attrs={
                'class': CLASS,
                'type': 'time'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        del self.fields['user']
        student_groups_value = self.fields.pop('student_groups')
        self.fields['student_groups'] = student_groups_value

    class Meta:
        model = Testing
        fields = '__all__'
