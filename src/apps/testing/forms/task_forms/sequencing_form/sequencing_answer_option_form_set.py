from django.forms import inlineformset_factory

from apps.testing.forms.task_forms.sequencing_form import SequencingAnswerOptionForm
from apps.testing.models.task_answer_options import SequencingAnswerOption
from apps.testing.models.tasks import Sequencing

SequencingAnswerOptionFormSet = inlineformset_factory(
    Sequencing,
    SequencingAnswerOption,
    form=SequencingAnswerOptionForm,
    exclude=['id', 'sequencing', ],
    extra=2,
    max_num=10
)
