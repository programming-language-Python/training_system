from typing import Iterable

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.views.generic.base import TemplateResponseMixin


class AbstractBaseTaskView(LoginRequiredMixin):
    answer_option_form_set: inlineformset_factory
    template_name: str

    def post(self, request, *args, **kwargs) -> redirect:
        task_form, answer_option_form_set = self._get_forms()
        if task_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(task_form, answer_option_form_set)
        else:
            return self.form_invalid(task_form, answer_option_form_set)

    def _get_forms(self) -> Iterable:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_valid(self, task_form, answer_option_form_set) -> redirect:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_invalid(self, task_form, answer_option_form_set) -> redirect:
        self.object = None
        return TemplateResponseMixin.render_to_response(
            self.get_context_data(
                form=task_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )
