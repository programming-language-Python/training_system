from collections.abc import MutableMapping
from typing import Mapping

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import ClosedQuestion, TaskType, OpenQuestion
from apps.testing.services import TaskService
from apps.testing.services.answer_option_service import AnswerOptionService


class AbstractTaskCreateView(LoginRequiredMixin, CreateView):
    answer_option_form_set = None
    template_name: str
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        fields = context['form'].fields
        context['form'].fields = self._get_task_fields_context_data(fields)
        context |= self._get_answer_option_context_data()
        context['btn_text'] = 'Создать задачу'
        return context

    def _get_task_fields_context_data(self, fields: Mapping) -> Mapping:
        task_service = TaskService(testing_pk=self.kwargs['testing_pk'])
        return task_service.set_initial_values_form_fields(fields)

    def _get_answer_option_context_data(self) -> Mapping:
        answer_option_service = AnswerOptionService(form_set=self.answer_option_form_set())
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def post(self, request, *args, **kwargs) -> redirect:
        task_form = self.form_class(request.POST)
        answer_option_form_set = self.answer_option_form_set(request.POST, request.FILES)
        if task_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(task_form, answer_option_form_set)
        else:
            return self.form_invalid(task_form, answer_option_form_set)

    def form_valid(self, task_form, answer_option_form_set) -> redirect:
        task = task_form.save(commit=False)
        task.task_type = self.get_task_type()
        task.save()
        answer_option_form_set.instance = task
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['testing_pk'])

    def get_task_type(self) -> TaskType:
        if self.model == ClosedQuestion:
            name = 'Закрытый вопрос'
        if self.model == OpenQuestion:
            name = 'Открытый вопрос'
        task_type, is_created = TaskType.objects.get_or_create(name=name)
        return task_type

    def form_invalid(self, task_form, answer_option_form_set) -> redirect:
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=task_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )
