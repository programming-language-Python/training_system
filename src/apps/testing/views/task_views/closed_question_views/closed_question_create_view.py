from apps.testing.abstractions.abstract_views import AbstractClosedQuestionCreateOrUpdateView, AbstractTaskCreateView


class ClosedQuestionCreateView(AbstractClosedQuestionCreateOrUpdateView, AbstractTaskCreateView):
    pass
