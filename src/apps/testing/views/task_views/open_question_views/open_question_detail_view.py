from apps.testing.abstractions.abstract_views import AbstractTaskDetailView
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionDetailView(AbstractTaskDetailView):
    model = OpenQuestion
    template_name = 'testing/task/open_question/open_question_detail.html'
