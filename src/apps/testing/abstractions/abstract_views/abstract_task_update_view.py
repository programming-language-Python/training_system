from collections.abc import MutableMapping
from typing import Mapping, Iterable, Type

from django.forms import inlineformset_factory, ModelForm
from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.abstractions.abstract_views import AbstractFormSetView
from apps.testing.constants import APP_NAME
from apps.testing.services.answer_option_service import AnswerOptionService
from apps.testing.utils.text import convert_from_PascalCase_to_snake_case


class AbstractTaskUpdateView(AbstractFormSetView, UpdateView):
    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= self._get_answer_option_context_data()
        context['btn_text'] = 'Обновить задачу'
        context['type'] = context['object'].task_type.name
        return context

    def _get_answer_option_context_data(self) -> Mapping:
        form_set = self.form_set(instance=self.get_object())
        form_set.extra = 0
        answer_option_service = AnswerOptionService(form_set)
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def _get_forms(self) -> Iterable[Type[ModelForm] | Type[inlineformset_factory]]:
        return (
            self.form_class(
                self.request.POST,
                instance=self.get_object()
            ),
            self.form_set(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        )

    def form_valid(self, task_form, answer_option_form_set) -> redirect:
        task_form.save()
        answer_option_form_set.save()
        class_name = convert_from_PascalCase_to_snake_case(task_form.instance.__class__.__name__)
        return redirect(f'{APP_NAME}:task_{class_name}_update', pk=self.kwargs['pk'])
