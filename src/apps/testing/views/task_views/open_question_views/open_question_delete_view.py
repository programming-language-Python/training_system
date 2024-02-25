from apps.testing.abstractions.abstract_views import AbstractTaskDeleteView
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionDeleteView(AbstractTaskDeleteView):
    model = OpenQuestion
