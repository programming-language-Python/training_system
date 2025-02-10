from collections.abc import MutableMapping
from typing import Mapping

from django.shortcuts import redirect
from django.views.generic import CreateView

from abstractions.abstract_views import AbstractFormSetView
from apps.testing.abstractions.abstract_views import AbstractTaskView, \
    AbstractTaskCreateOrUpdateView
from apps.testing.constants import APP_NAME
from apps.testing.services import TaskService
from apps.testing.services.answer_option_service import AnswerOptionService
from apps.testing.types import ValidTask, TaskType
from custom_types import InlineFormSetFactory


class AbstractTaskCreateView(AbstractTaskView, AbstractTaskCreateOrUpdateView, AbstractFormSetView, CreateView):
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= self._get_answer_option_context_data()
        context |= {
            'btn_text': 'Создать задачу',
            'task_type': TaskType(self.kwargs['type']),
            'additional_form': self.additional_form,
            'answer_options_template_name': self.answer_options_template_name
        }
        return context

    def _get_answer_option_context_data(self) -> Mapping:
        answer_option_service = AnswerOptionService(form_set=self.form_set())
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def _get_forms(self) -> InlineFormSetFactory:
        form_data = {
            'form': self.form_class(self.request.POST),
            'form_set': self.form_set(
                self.request.POST,
                self.request.FILES,
            )
        }
        if self.additional_form:
            form_data['additional_form'] = self.additional_form(self.request.POST)
        return InlineFormSetFactory(**form_data)

    def form_valid(self, task_forms: InlineFormSetFactory) -> redirect:
        valid_task = ValidTask(
            task_forms=task_forms,
            type=self.kwargs['type'],
            testing_pk=self.kwargs['testing_pk']
        )
        task_service = TaskService()
        task_service.create(valid_task)
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['testing_pk'])
