from typing import Mapping

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from apps.testing_by_code.forms import TaskForm, SettingForm
from apps.testing_by_code.models import Testing, SolvingTesting
from apps.testing_by_code.services import TestingService
from apps.testing_by_code.services.task_service import TaskService
from apps.testing_by_code.constants import APP_NAME
from mixins import ContextMixin, LoginMixin


class TestingDetailView(LoginMixin, ContextMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs) -> Mapping[str, SolvingTesting]:
        is_teacher_ = self.request.user.is_teacher()
        if is_teacher_:
            context = super().get_context_data(**kwargs)
            context |= self.get_testing_detail_data(
                is_solving_testing=kwargs['object'].testing_by_code_solving_testing_set.exists()
            )
            context |= {'add_task_form_url': f'{self.APP_NAME}:add_task_form'}
        else:
            testing = kwargs['object']
            context = self._start_testing(testing)
        return context

    def _start_testing(self, testing: Testing) -> Mapping[str, SolvingTesting]:
        testing_service = TestingService(
            student=self.request.user.student,
            testing=testing
        )
        return testing_service.start()

    @staticmethod
    def post(request, *args, **kwargs) -> None:
        task_form = TaskForm(request.POST or None)
        setting_form = SettingForm(request.POST or None)
        context = {
            'task_form': task_form,
            'setting_form': setting_form
        }
        is_valid_forms = task_form.is_valid() and setting_form.is_valid()
        if is_valid_forms:
            user = request.user
            forms = context
            testing = get_object_or_404(Testing, pk=kwargs['pk'])
            task_service = TaskService(user, forms, testing)
            task_service.add()
            return redirect('testing_by_code:task_detail', pk=task_service.get_pk())
        return render(request, 'testing_by_code/task_form.html', context)
