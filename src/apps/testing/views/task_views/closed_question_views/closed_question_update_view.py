from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView
from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionUpdateView(AbstractTaskUpdateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    answer_option_form_set = ClosedQuestionAnswerOptionFormSet
    template_name = 'testing/task/closed_question/closed_question_create_or_update.html'
