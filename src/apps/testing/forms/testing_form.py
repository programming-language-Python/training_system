from django import forms

from abstractions.abstract_forms import AbstractTestingForm
from apps.base_testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD
from apps.testing.constants import MAX_PROBABILITY_OF_GUESSING
from apps.testing.models import Testing


class TestingForm(AbstractTestingForm):
    class Meta(AbstractTestingForm.Meta):
        CLASS = 'uk-margin-small uk-input uk-width-small'
        model = Testing
        widgets = AbstractTestingForm.Meta.widgets | {
            'number': forms.NumberInput(attrs={
                'class': CLASS,
            }),
            'probability_of_guessing': forms.NumberInput(attrs={
                'class': CLASS,
                'max': MAX_PROBABILITY_OF_GUESSING,
                'min': 0,
                'step': '0.01'
            }),
            'assessment_threshold': forms.NumberInput(attrs={
                'class': CLASS,
                'min': MIN_ASSESSMENT_THRESHOLD,
                'max': MAX_ASSESSMENT_THRESHOLD,
            }),
        }
        exclude = ('date_of_deletion', 'max_score', 'journal')
