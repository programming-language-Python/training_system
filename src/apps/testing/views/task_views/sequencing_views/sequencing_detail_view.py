from apps.testing.abstractions.abstract_views import AbstractTaskDetailView
from apps.testing.models.tasks import Sequencing


class SequencingDetailView(AbstractTaskDetailView):
    model = Sequencing
    template_name = 'testing/task/sequencing/sequencing_detail.html'
