from apps.testing.abstractions.abstract_views import AbstractTaskWithChoiceCreateOrUpdateView, \
    AbstractTaskCreateView


class SequencingCreateView(AbstractTaskWithChoiceCreateOrUpdateView, AbstractTaskCreateView):
    pass
