from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from formtools.wizard.views import SessionWizardView


class TestingDetailStudentView(SessionWizardView):
    template_name = 'testing/testing_detail_student.html'

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        page = int(self.steps.current)
        solving_task = self.initial_dict[page]['solving_task']
        solving_task.set_start_passage()
        context['testing_title'] = self.initial_dict['solving_testing'].testing.title
        context['task_description'] = mark_safe(solving_task.task.description)
        return context

    def get_form_initial(self, step):
        page = int(step)
        return self.initial_dict[page]

    def done(self, task_forms, **kwargs) -> redirect:
        return self.initial_dict['testing_service'].end_testing(
            task_forms
        )

    def post(self, *args, **kwargs):
        current_index = self.get_step_index(self.steps.current)
        go_to_step = self.request.POST.get('wizard_goto_step', None)
        goto_index = self.get_step_index(go_to_step) if self.get_step_index(go_to_step) == 'NoneType' else -1

        form = self.get_form(data=self.request.POST)
        if current_index > goto_index:
            if form.is_valid():
                solving_task = self.initial_dict[current_index]['solving_task']
                self.initial_dict['testing_service'].update_solving_task(
                    solving_task,
                    form.cleaned_data
                )
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(self.steps.current, self.process_step_files(form))
        else:
            return self.render(form)
        return super(TestingDetailStudentView, self).post(*args, **kwargs)
