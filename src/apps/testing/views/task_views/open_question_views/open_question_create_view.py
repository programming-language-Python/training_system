from apps.testing.abstractions.abstract_views import AbstractTaskCreateView
from apps.testing.forms.task_forms.open_question_form import OpenQuestionForm, OpenQuestionAnswerOptionFormSet
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionCreateView(AbstractTaskCreateView):
    model = OpenQuestion
    form_class = OpenQuestionForm
    form_set = OpenQuestionAnswerOptionFormSet
    template_name = 'testing/task/open_question/open_question_create_or_update.html'
    answer_options_template_name = 'testing/inc/task/_open_question_table_answer_options.html'
