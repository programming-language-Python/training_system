from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView, \
    AbstractTaskWithChoiceCreateOrUpdateView


class SequencingUpdateView(AbstractTaskWithChoiceCreateOrUpdateView, AbstractTaskUpdateView):
    pass
