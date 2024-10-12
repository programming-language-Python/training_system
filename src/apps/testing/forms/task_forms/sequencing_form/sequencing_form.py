from django import forms

from apps.testing.abstractions.abstract_forms import AbstractTaskForm
from apps.testing.models.tasks import Sequencing


class SequencingForm(AbstractTaskForm):
    task_name = forms.CharField(initial='sequencing', widget=forms.HiddenInput())

    class Meta(AbstractTaskForm.Meta):
        model = Sequencing
