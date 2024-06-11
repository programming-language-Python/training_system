from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING, Type, TypeAlias

from django.forms import ModelForm

if TYPE_CHECKING:
    from apps.testing.services import TestingService
    from apps.testing.models.solving_tasks import SolvingOpenQuestion, SolvingClosedQuestion
    from apps.testing.models.tasks import OpenQuestion, ClosedQuestion

Id: TypeAlias = int
Description: TypeAlias = str
Task: TypeAlias = 'OpenQuestion' or 'ClosedQuestion'
SolvingTask: TypeAlias = 'SolvingOpenQuestion' or 'SolvingClosedQuestion'


@dataclass
class TaskType:
    name: str
    url: str


@dataclass
class SolvingTestingData:
    task_forms: Sequence[Type[ModelForm]]
    task_form_data: 'TaskFormData'


@dataclass
class TaskFormData:
    testing_service: 'TestingService'
    pages: Sequence['PageData']


@dataclass
class PageData:
    answer: str
    solving_task: SolvingTask
