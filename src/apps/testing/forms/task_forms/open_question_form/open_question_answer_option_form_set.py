from django.forms import inlineformset_factory

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerOptionForm
from apps.testing.models.tasks import OpenQuestion
from apps.testing.models.tasks.open_question import OpenQuestionAnswerOption

OpenQuestionAnswerOptionFormSet = inlineformset_factory(
    OpenQuestion,
    OpenQuestionAnswerOption,
    form=OpenQuestionAnswerOptionForm,
    exclude=['id', 'open_question', ],
    extra=1,
    max_num=10
)
