from typing import Type

from django.forms import ModelForm

from apps.testing.forms.task_forms import TaskForm


class AbstractTaskCreateOrUpdateView:
    form_class = TaskForm
    additional_form: Type[ModelForm] | None = None
