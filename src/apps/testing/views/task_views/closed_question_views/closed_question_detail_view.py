from apps.testing.abstractions.abstract_views.abstract_task_detail_view import AbstractTaskDetailView
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionDetailView(AbstractTaskDetailView):
    model = ClosedQuestion
    template_name = 'testing/task/closed_question/closed_question_detail.html'
