from typing import Type

from django.forms import ModelForm
from django.http import HttpResponse
from django.template.loader import render_to_string

from apps.testing.forms.task_forms import TaskForm


class AbstractTaskCreateOrUpdateView:
    form_class = TaskForm
    additional_form: Type[ModelForm] | None = None

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Для UpdateView
            self.object = self.get_object()
        else:
            # Для CreateView
            self.object = None
        if request.GET.get('quantity-answer-options-add'):
            context = self.get_context_data()
            html = render_to_string(self.answer_options_template_name, context, request=request)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)
