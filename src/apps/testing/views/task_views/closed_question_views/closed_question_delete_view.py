from apps.testing.abstractions.abstract_views import AbstractTaskDeleteView
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionDeleteView(AbstractTaskDeleteView):
    model = ClosedQuestion
