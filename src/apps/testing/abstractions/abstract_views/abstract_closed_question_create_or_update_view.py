from apps.testing.forms.answer_options_forms_set import AnswerOptionFormSet
from apps.testing.forms.task_forms import ClosedQuestionForm


class AbstractClosedQuestionCreateOrUpdateView:
    additional_form = ClosedQuestionForm
    form_set = AnswerOptionFormSet
    template_name = 'testing/task/task_with_choice_create_or_update.html'
    table_answer_options_template_name = 'testing/inc/task/answer_options/_table_closed_question_answer_options.html'
    answer_options_template_name = 'testing/inc/task/answer_options/_closed_question_answer_options.html'
