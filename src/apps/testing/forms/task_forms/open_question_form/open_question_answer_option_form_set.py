from django.forms import inlineformset_factory

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerOptionForm
from apps.testing.models.task_answer_options import OpenQuestionAnswerOption
from apps.testing.models.tasks import OpenQuestion

OpenQuestionAnswerOptionFormSet = inlineformset_factory(
    OpenQuestion,
    OpenQuestionAnswerOption,
    form=OpenQuestionAnswerOptionForm,
    exclude=['id', 'open_question', ],
    extra=1,
    max_num=10
)
