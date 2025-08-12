from apps.testing.abstractions.abstract_views import AbstractTaskCreateView, AbstractOpenQuestionCreateOrUpdateView


class OpenQuestionCreateView(AbstractOpenQuestionCreateOrUpdateView, AbstractTaskCreateView):
    pass
