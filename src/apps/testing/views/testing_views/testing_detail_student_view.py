from formtools.wizard.views import SessionWizardView

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerForm


class TestingDetailStudentView(SessionWizardView):
    template_name = 'testing/testing_detail_student.html'

    def done(self, form_list, **kwargs):
        print(form_list)

    def post(self, *args, **kwargs):
        go_to_step = self.request.POST.get('wizard_goto_step', None)  # get the step name
        form = self.get_form(data=self.request.POST)

        current_index = self.get_step_index(self.steps.current)
        goto_index = self.get_step_index(go_to_step) if self.get_step_index(go_to_step) == 'NoneType' else -1

        if current_index > goto_index:
            if form.is_valid():
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(self.steps.current, self.process_step_files(form))
        else:
            return self.render(form)
        return super(TestingDetailStudentView, self).post(*args, **kwargs)
