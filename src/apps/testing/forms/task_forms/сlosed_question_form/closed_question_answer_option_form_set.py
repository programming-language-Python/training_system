from django.forms import inlineformset_factory

from apps.testing.forms.task_forms.сlosed_question_form.closed_question_answer_option_form import \
    ClosedQuestionAnswerOptionForm
from apps.testing.models import ClosedQuestion
from apps.testing.models.tasks.closed_question import ClosedQuestionAnswerOption

ClosedQuestionAnswerOptionFormSet = inlineformset_factory(
    ClosedQuestion,
    ClosedQuestionAnswerOption,
    form=ClosedQuestionAnswerOptionForm,
    exclude=['id', 'closed_question', ],
    extra=2,
    max_num=10
)
