from apps.testing.abstractions.abstract_forms import AbstractAnswerOptionWithCheckboxForm
from apps.testing.models.task_answer_options import SequencingAnswerOption


class SequencingAnswerOptionForm(AbstractAnswerOptionWithCheckboxForm):
    class Meta(AbstractAnswerOptionWithCheckboxForm.Meta):
        model = SequencingAnswerOption
        fields = AbstractAnswerOptionWithCheckboxForm.Meta.fields + ('sequencing',)
