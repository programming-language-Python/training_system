from django.forms import inlineformset_factory

from apps.testing.forms.answer_options_forms import OpenQuestionAnswerOptionForm
from apps.testing.models import Task
from apps.testing.models.task_answer_options import OpenQuestionAnswerOption

OpenQuestionAnswerOptionFormSet = inlineformset_factory(
    Task,
    OpenQuestionAnswerOption,
    form=OpenQuestionAnswerOptionForm,
    exclude=['id', ],
    extra=1,
    max_num=10
)
