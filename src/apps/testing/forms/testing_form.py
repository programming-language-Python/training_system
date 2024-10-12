from django import forms

from abstractions.abstract_forms import AbstractTestingForm
from apps.testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD, MAX_LIKELIHOOD_GUESSING_ANSWERS
from apps.testing.models import Testing


class TestingForm(AbstractTestingForm):
    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        student_groups_value = self.fields.pop('student_groups')
        self.fields['student_groups'] = student_groups_value

    class Meta(AbstractTestingForm.Meta):
        CLASS = 'uk-margin-small uk-input uk-width-small'
        model = Testing
        widgets = AbstractTestingForm.Meta.widgets | {
            'number': forms.NumberInput(attrs={
                'class': CLASS,
            }),
            'likelihood_guessing_answers': forms.NumberInput(attrs={
                'class': CLASS,
                'max': MAX_LIKELIHOOD_GUESSING_ANSWERS,
                'min': 0,
                'step': '0.01'
            }),
            'assessment_threshold': forms.NumberInput(attrs={
                'class': CLASS,
                'min': MIN_ASSESSMENT_THRESHOLD,
                'max': MAX_ASSESSMENT_THRESHOLD,
            }),
        }
        fields = '__all__'
        exclude = ['teacher', 'date_of_deletion', ]
