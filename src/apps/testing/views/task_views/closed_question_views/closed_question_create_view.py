from collections.abc import MutableMapping

from django.shortcuts import redirect
from django.views.generic import CreateView

from apps.testing.constants import APP_NAME
from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models import ClosedQuestion
from apps.testing.services import TaskService
from apps.testing.services.answer_option_service import AnswerOptionService


class ClosedQuestionCreateView(CreateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    template_name = 'testing/task/closed_question_create_or_update.html'
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs) -> MutableMapping:
        task_service = TaskService(testing_pk=self.kwargs['testing_pk'])
        answer_option_service = AnswerOptionService(form_set=ClosedQuestionAnswerOptionFormSet())
        context = super().get_context_data(**kwargs)
        context['form'].fields = task_service.set_initial_values_form_fields(fields=context['form'].fields)
        quantity_answer_options_add = self.request.GET.get('quantity-answer-options-add')
        context |= answer_option_service.get_context(quantity_answer_options_add)
        context['btn_text'] = 'Создать задачу'
        return context

    def post(self, request, *args, **kwargs) -> redirect:
        closed_question_form = self.form_class(request.POST)
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(request.POST, request.FILES)
        if closed_question_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(closed_question_form, answer_option_form_set)
        else:
            return self.form_invalid(closed_question_form, answer_option_form_set)

    def form_valid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ) -> redirect:
        closed_question = closed_question_form.save()
        answer_option_form_set.instance = closed_question
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['testing_pk'])

    def form_invalid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ) -> redirect:
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=closed_question_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )
