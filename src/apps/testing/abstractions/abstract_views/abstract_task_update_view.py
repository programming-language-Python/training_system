from collections.abc import MutableMapping
from typing import Mapping

from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.abstractions.abstract_views import AbstractFormSetView, AbstractTaskView, \
    AbstractTaskCreateOrUpdateView
from apps.testing.constants import APP_NAME
from apps.testing.services import TaskService
from apps.testing.services.answer_option_service import AnswerOptionService
from apps.testing.types import InlineFormSetFactory


class AbstractTaskUpdateView(AbstractTaskView, AbstractTaskCreateOrUpdateView, AbstractFormSetView, UpdateView):
    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= self._get_answer_option_context_data()
        if self.object.additional_model:
            instance = self.object.additional_model
            context['additional_form'] = self.additional_form(instance=instance)
        context |= {
            'btn_text': 'Обновить задачу',
            'task_type': self.object.task_type,
            'answer_options_template_name': self.answer_options_template_name
        }
        return context

    def _get_answer_option_context_data(self) -> Mapping:
        form_set = self.form_set(instance=self.get_object())
        form_set.extra = 0
        answer_option_service = AnswerOptionService(form_set)
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def _get_forms(self) -> InlineFormSetFactory:
        form_data = {
            'form': self.form_class(
                self.request.POST,
                instance=self.get_object()
            ),
            'form_set': self.form_set(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        }
        if self.additional_form:
            form_data['additional_form'] = self.additional_form(self.request.POST)
        return InlineFormSetFactory(**form_data)

    def form_valid(self, task_forms: InlineFormSetFactory) -> redirect:
        task_service = TaskService()
        task_service.update(task_forms)
        task = task_forms.form.instance
        task_type = task.en_type
        return redirect(f'{APP_NAME}:task_{task_type}_update', pk=self.kwargs['pk'])
