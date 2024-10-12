from apps.testing.abstractions.abstract_views import AbstractTaskCreateView
from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionCreateView(AbstractTaskCreateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    form_set = ClosedQuestionAnswerOptionFormSet
    template_name = 'testing/task/task_with_answer_option_with_checkbox.html'
    answer_options_template_name = 'testing/inc/task/table/_table_answer_option_with_checkbox.html'
