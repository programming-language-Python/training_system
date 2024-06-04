from django.forms import modelformset_factory

from apps.testing.models.task_answer_options import ClosedQuestionAnswerOption

SolvingClosedQuestionFormSet = modelformset_factory(
    ClosedQuestionAnswerOption,
    fields=('description', 'is_correct')
)
