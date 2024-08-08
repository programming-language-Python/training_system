from collections.abc import MutableMapping
from typing import Mapping, Iterable, Type

from django.forms import inlineformset_factory, ModelForm
from django.shortcuts import redirect
from django.views.generic import CreateView

from apps.testing.abstractions.abstract_views import AbstractFormSetView
from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import TaskType
from apps.testing.services import TaskService
from apps.testing.services.answer_option_service import AnswerOptionService


class AbstractTaskCreateView(AbstractFormSetView, CreateView):
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        fields = context['form'].fields
        context['form'].fields = self._get_task_fields_context_data(fields)
        context |= self._get_answer_option_context_data()
        context['btn_text'] = 'Создать задачу'
        context['type'] = self.kwargs['type']
        return context

    def _get_task_fields_context_data(self, fields: Mapping) -> Mapping:
        task_service = TaskService(testing_pk=self.kwargs['testing_pk'])
        return task_service.set_initial_values_form_fields(fields)

    def _get_answer_option_context_data(self) -> Mapping:
        answer_option_service = AnswerOptionService(form_set=self.form_set())
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def _get_forms(self) -> Iterable[Type[ModelForm] | Type[inlineformset_factory]]:
        return (
            self.form_class(self.request.POST),
            self.form_set(
                self.request.POST,
                self.request.FILES,
            )
        )

    def form_valid(self, task_form, answer_option_form_set) -> redirect:
        task = task_form.save(commit=False)
        task.task_type, is_created = TaskType.objects.get_or_create(name=self.kwargs['type'])
        task.save()
        answer_option_form_set.instance = task
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['testing_pk'])
