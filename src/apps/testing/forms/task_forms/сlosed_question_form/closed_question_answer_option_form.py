from apps.testing.abstractions.abstract_forms import AbstractAnswerOptionWithCheckboxForm
from apps.testing.models.task_answer_options import ClosedQuestionAnswerOption


class ClosedQuestionAnswerOptionForm(AbstractAnswerOptionWithCheckboxForm):
    class Meta(AbstractAnswerOptionWithCheckboxForm.Meta):
        model = ClosedQuestionAnswerOption
        fields = AbstractAnswerOptionWithCheckboxForm.Meta.fields + ('closed_question',)
