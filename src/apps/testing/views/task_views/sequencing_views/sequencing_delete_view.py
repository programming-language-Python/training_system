from apps.testing.abstractions.abstract_views import AbstractTaskDeleteView
from apps.testing.models.tasks import Sequencing


class SequencingDeleteView(AbstractTaskDeleteView):
    model = Sequencing
