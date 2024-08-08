from django import forms

from apps.testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD
from apps.testing.models import MaxScore


class MaxScoreForm(forms.ModelForm):
    ATTRS = {
        'class': 'uk-margin-small uk-input uk-width-small',
        'min': MIN_ASSESSMENT_THRESHOLD,
        'max': MAX_ASSESSMENT_THRESHOLD
    }
    max_score_meta = MaxScore._meta

    five = forms.IntegerField(
        label=max_score_meta.get_field('five').verbose_name,
        widget=forms.NumberInput(attrs=ATTRS)
    )
    four = forms.IntegerField(
        label=max_score_meta.get_field('four').verbose_name,
        widget=forms.NumberInput(attrs=ATTRS)
    )
    three = forms.IntegerField(
        label=max_score_meta.get_field('three').verbose_name,
        widget=forms.NumberInput(attrs=ATTRS)
    )
    two = forms.IntegerField(
        label=max_score_meta.get_field('two').verbose_name,
        widget=forms.NumberInput(attrs=ATTRS)
    )

    class Meta:
        model = MaxScore
        exclude = ['testing']
