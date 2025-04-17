from typing import MutableMapping

from apps.testing.abstractions.abstract_views import AbstractTaskDetailView
from apps.testing.models.task_answer_options import AnswerOption
from services import get_model_fields


class SequencingDetailView(AbstractTaskDetailView):
    template_name = 'testing/task/closed_question/closed_question_detail.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context |= {
            'answer_options': self.object.answer_option_set.all(),
            'fields_answer_option': get_model_fields(
                model=AnswerOption,
                excluded_fields=['id', 'task']
            )
        }
        return context
