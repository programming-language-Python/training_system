from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView
from apps.testing.forms.task_forms.open_question_form import OpenQuestionForm, OpenQuestionAnswerOptionFormSet
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionUpdateView(AbstractTaskUpdateView):
    model = OpenQuestion
    form_class = OpenQuestionForm
    form_set = OpenQuestionAnswerOptionFormSet
    template_name = 'testing/task/open_question/open_question_create_or_update.html'
