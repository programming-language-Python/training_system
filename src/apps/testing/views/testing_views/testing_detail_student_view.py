from typing import Sequence

from django.forms import MultipleChoiceField
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from formtools.wizard.views import SessionWizardView

from apps.testing.models import SolvingTask
from apps.testing.services import TestingService, TaskService
from apps.testing.services import ClosedQuestionService


class TestingDetailStudentView(SessionWizardView):
    template_name = 'testing/testing_detail_student.html'
    testing_service: TestingService = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_service = TaskService()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context |= self._get_testing_context_data() | self._get_task_context_data()
        return context

    def _get_testing_context_data(self) -> dict[str, str]:
        solving_testing = self.initial_dict[0].solving_testing
        testing_context_data = {'testing_title': solving_testing.testing.title, }
        if solving_testing.get_end_passage() is not None:
            testing_context_data |= {
                'end_passage': solving_testing.get_end_passage_iso_format(),
                'duration': round(solving_testing.get_duration().total_seconds()),
            }
        return testing_context_data

    def _get_task_context_data(self) -> dict[str, str]:
        page = int(self.steps.current)
        solving_task = self.initial_dict[page]
        solving_task.set_start_passage()
        return {'task_description': mark_safe(solving_task.task.description)}

    def get_form_initial(self, step):
        return self._set_answer_option_form(step)

    def _set_answer_option_form(self, step: str) -> dict:
        page = int(step)
        answer_field = self.form_list[step].base_fields['answer']
        solving_task = self.initial_dict[page]

        if isinstance(answer_field, MultipleChoiceField):
            task = solving_task.task
            answer_field.choices = self.task_service.get_answer_field_choices(
                task_service=ClosedQuestionService(task)
            )
        return self.initial_dict

    def done(self, task_forms: Sequence[SolvingTask], **kwargs) -> redirect:
        return self.testing_service.end_testing(task_forms)

    def post(self, *args, **kwargs):
        current_index = self.get_step_index(self.steps.current)
        go_to_step = self.request.POST.get('wizard_goto_step', None)
        goto_index = self.get_step_index(go_to_step) if self.get_step_index(go_to_step) == 'NoneType' else -1

        form = self.get_form(data=self.request.POST)
        if current_index > goto_index:
            if form.is_valid():
                solving_task = self.initial_dict[current_index]
                answer = form.cleaned_data['answer']
                self.task_service.set_answer(solving_task, answer)
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(self.steps.current, self.process_step_files(form))
            else:
                return self.render(form)
        return super(TestingDetailStudentView, self).post(*args, **kwargs)
