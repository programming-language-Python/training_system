from apps.testing.abstractions.abstract_views import AbstractTaskCreateView
from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionCreateView(AbstractTaskCreateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    answer_option_form_set = ClosedQuestionAnswerOptionFormSet
