from apps.testing.abstractions.abstract_views import AbstractTaskDetailView
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionDetailView(AbstractTaskDetailView):
    model = ClosedQuestion
    template_name = 'testing/task/closed_question/closed_question_detail.html'
