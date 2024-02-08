from collections.abc import MutableMapping
from typing import Mapping

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.constants import APP_NAME
from apps.testing.services.answer_option_service import AnswerOptionService
from apps.testing.utils.text import convert_from_PascalCase_to_snake_case


class AbstractTaskUpdateView(LoginRequiredMixin, UpdateView):
    answer_option_form_set = None
    template_name = 'testing/task/closed_question_create_or_update.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= self._get_answer_option_context_data()
        context['btn_text'] = 'Обновить задачу'
        return context

    def _get_answer_option_context_data(self) -> Mapping:
        form_set = self.answer_option_form_set(instance=self.get_object())
        form_set.extra = 0
        answer_option_service = AnswerOptionService(form_set)
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        return answer_option_service.get_context_data(quantity_answer_options_add)

    def post(self, request, *args, **kwargs) -> redirect:
        task_form = self.form_class(request.POST, instance=self.get_object())
        answer_option_form_set = self.answer_option_form_set(
            request.POST,
            request.FILES,
            instance=self.get_object()
        )
        if task_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(task_form, answer_option_form_set)
        else:
            return self.form_invalid(task_form, answer_option_form_set)

    def form_valid(self, task_form, answer_option_form_set) -> redirect:
        task_form.save()
        answer_option_form_set.save()
        class_name = convert_from_PascalCase_to_snake_case(task_form.instance.__class__.__name__)
        return redirect(f'{APP_NAME}:task_{class_name}_update', pk=self.kwargs['pk'])

    def form_invalid(self, task_form, answer_option_form_set) -> redirect:
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=task_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )
