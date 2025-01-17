from typing import Type

from apps.testing.forms.solving_task_form import SolvingTaskForm, SolvingTaskWithChoiceForm
from apps.testing.types import TaskType


class TaskFormService:
    @staticmethod
    def get_solving_form(task_type: str | TaskType) -> Type[SolvingTaskForm]:
        match task_type:
            case TaskType.CLOSED_QUESTION | TaskType.SEQUENCING:
                return SolvingTaskWithChoiceForm
            case TaskType.OPEN_QUESTION:
                return SolvingTaskForm
