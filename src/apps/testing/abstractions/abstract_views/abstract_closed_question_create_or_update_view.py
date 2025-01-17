from apps.testing.abstractions.abstract_views import AbstractTaskWithChoiceCreateOrUpdateView
from apps.testing.forms.task_forms import ClosedQuestionForm


class AbstractClosedQuestionCreateOrUpdateView(AbstractTaskWithChoiceCreateOrUpdateView):
    additional_form = ClosedQuestionForm
