import datetime

from django.shortcuts import get_object_or_404
from formtools.wizard.views import SessionWizardView

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerForm
from apps.testing.models import SolvingTesting
from apps.testing.models.tasks import OpenQuestion


class TestingDetailStudentView(SessionWizardView):
    template_name = 'testing/testing_detail_student.html'

    def get_form_initial(self, step):
        initial = self.initial_dict.get(int(step))
        return initial

    # def done(self, task_forms, **kwargs):
    #     solving_testing = SolvingTesting.objects.filter(pk=kwargs['completed_testing_pk'])
    #     solving_testing.update(end_passage=datetime.datetime.now())
    #
    #     for task_form in task_forms:
    #         if isinstance(task_form, OpenQuestionAnswerForm):
    #             self._create_completed_open_question(task_form, solving_testing)
    #
    # @staticmethod
    # def _create_completed_open_question(task_form: OpenQuestionAnswerForm, solving_testing: SolvingTesting):
    #     open_question = get_object_or_404(OpenQuestion, pk=task_form.initial['task_pk'])
    #     student_answer = task_form.cleaned_data['student_answer']
    #     is_correct = open_question.open_question_answer_option_set.filter(
    #         correct_answer=student_answer
    #     ).exists()
    #
    #     completed_open_question = task_form.save(commit=False)
    #     completed_open_question.solving_testing = solving_testing
    #     completed_open_question.save()
    #
    #     open_question_data = open_question.open_question_answer_option_set.values()
    #     for open_question in open_question_data:
    #         OpenQuestionAnswerOptionCorrect.objects.create(
    #             correct_answer=open_question['correct_answer'],
    #             completed_open_question=completed_open_question
    #         )

    def post(self, *args, **kwargs):
        go_to_step = self.request.POST.get('wizard_goto_step', None)
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
