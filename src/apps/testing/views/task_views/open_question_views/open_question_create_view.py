from apps.testing.abstractions.abstract_views import AbstractTaskCreateView
from apps.testing.forms.answer_options_forms_set import OpenQuestionAnswerOptionFormSet


class OpenQuestionCreateView(AbstractTaskCreateView):
    form_set = OpenQuestionAnswerOptionFormSet
    template_name = 'testing/task/open_question/open_question_create_or_update.html'
    answer_options_template_name = 'testing/inc/task/answer_options/_open_question_answer_options.html'
