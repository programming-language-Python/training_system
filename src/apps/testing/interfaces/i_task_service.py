from typing import Protocol, Iterable

from apps.testing.models.task_answer_options import AnswerOption


class ITaskService(Protocol):
    def get_answer_options(self) -> Iterable[AnswerOption]:
        pass
