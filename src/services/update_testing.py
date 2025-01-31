from django.forms import ModelForm

from apps.base_testing.forms import MaxScoreForm
from apps.base_testing.models import MaxScore


def update_testing(form: ModelForm, max_score_form: MaxScoreForm):
    if max_score_form.changed_data:
        testing = form.save(commit=False)
        max_score, _ = MaxScore.objects.get_or_create(**max_score_form.cleaned_data)
        testing.max_score = max_score
        testing.save()
    else:
        form.save()
