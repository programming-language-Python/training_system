from typing import MutableMapping

from apps.testing.abstractions.abstract_views import AbstractTaskDetailView


class OpenQuestionDetailView(AbstractTaskDetailView):
    template_name = 'testing/task/open_question/open_question_detail.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= {
            'answer_options': self.object.open_question_answer_option_set.all().values_list('correct_answer')
        }
        return context
