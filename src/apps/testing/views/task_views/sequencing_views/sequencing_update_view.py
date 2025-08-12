from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView, AbstractSequencingCreateOrUpdateView


class SequencingUpdateView(AbstractSequencingCreateOrUpdateView, AbstractTaskUpdateView):
    pass
