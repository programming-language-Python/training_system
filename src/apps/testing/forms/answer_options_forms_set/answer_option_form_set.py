from django.forms import inlineformset_factory

from apps.testing.forms.answer_options_forms import AnswerOptionForm
from apps.testing.models import Task
from apps.testing.models.task_answer_options import AnswerOption

AnswerOptionFormSet = inlineformset_factory(
    Task,
    AnswerOption,
    form=AnswerOptionForm,
    exclude=['id', ],
    extra=2,
    max_num=10
)
