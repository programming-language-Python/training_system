from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.constants import APP_NAME
from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models import ClosedQuestion


class ClosedQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    template_name = 'testing/task/closed_question_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(instance=self.get_object())
        answer_option_form_set.extra = 0
        context['answer_option_form_set'] = answer_option_form_set
        for form in context['answer_option_form_set'].forms:
            form.fields['closed_question'].widget.attrs = {'data-name': 'closed-question'}
            form.fields['DELETE'].widget.attrs = {'data-name': 'delete'}
        context['btn_text'] = 'Обновить задачу'
        return context

    def post(self, request, *args, **kwargs):
        closed_question_form = self.form_class(request.POST, instance=self.get_object())
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(
            request.POST,
            request.FILES,
            instance=self.get_object()
        )
        if closed_question_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(closed_question_form, answer_option_form_set)
        else:
            return self.form_invalid(closed_question_form, answer_option_form_set)

    def form_valid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        closed_question_form.save()
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:task_closed_question_update', pk=self.kwargs['pk'])

    def form_invalid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=closed_question_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )
