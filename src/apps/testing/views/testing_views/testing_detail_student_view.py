from dataclasses import asdict
from typing import Sequence

from django.forms import MultipleChoiceField
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from formtools.wizard.views import SessionWizardView

from apps.testing.types import TaskFormData, SolvingTask


class TestingDetailStudentView(SessionWizardView):
    template_name = 'testing/testing_detail_student.html'
    initial_dict: TaskFormData

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        page = int(self.steps.current)
        solving_task = self.initial_dict.pages[page].solving_task
        solving_task.set_start_passage()
        solving_testing = self.initial_dict.testing_service.get_solving_testing()
        context['testing_title'] = solving_testing.testing.title
        context['task_description'] = mark_safe(solving_task.task.description)
        return context

    def get_form_initial(self, step):
        page = int(step)
        answer_field = self.form_list[step].base_fields['answer']
        if isinstance(answer_field, MultipleChoiceField):
            answer_field.choices = self.initial_dict.pages[page].solving_task.task.get_set_answer_options()
        return asdict(self.initial_dict.pages[page])

    def done(self, task_forms: Sequence[SolvingTask], **kwargs) -> redirect:
        return self.initial_dict.testing_service.end_testing(task_forms)

    def post(self, *args, **kwargs):
        current_index = self.get_step_index(self.steps.current)
        go_to_step = self.request.POST.get('wizard_goto_step', None)
        goto_index = self.get_step_index(go_to_step) if self.get_step_index(go_to_step) == 'NoneType' else -1

        form = self.get_form(data=self.request.POST)
        if current_index > goto_index:
            if form.is_valid():
                solving_task = self.initial_dict.pages[current_index].solving_task
                self.initial_dict.testing_service.update_solving_task(
                    solving_task,
                    form.cleaned_data
                )
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(self.steps.current, self.process_step_files(form))
            else:
                return self.render(form)
        return super(TestingDetailStudentView, self).post(*args, **kwargs)
