from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView, AbstractClosedQuestionCreateOrUpdateView


class ClosedQuestionUpdateView(AbstractClosedQuestionCreateOrUpdateView, AbstractTaskUpdateView):
    pass
