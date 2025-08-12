from apps.testing.abstractions.abstract_views import AbstractTaskCreateView, AbstractSequencingCreateOrUpdateView


class SequencingCreateView(AbstractSequencingCreateOrUpdateView, AbstractTaskCreateView):
    pass
