from django import forms

from apps.base_testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD
from apps.base_testing.models import MaxScore


class MaxScoreForm(forms.ModelForm):
    class Meta:
        model = MaxScore
        number_input = forms.NumberInput(attrs={
            'class': 'uk-margin-small uk-input uk-width-small',
            'min': MIN_ASSESSMENT_THRESHOLD,
            'max': MAX_ASSESSMENT_THRESHOLD
        })
        widgets = {
            'five': number_input,
            'four': number_input,
            'three': number_input,
            'two': number_input
        }
        fields = '__all__'
