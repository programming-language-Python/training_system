from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView, AbstractOpenQuestionCreateOrUpdateView


class OpenQuestionUpdateView(AbstractOpenQuestionCreateOrUpdateView, AbstractTaskUpdateView):
    pass
