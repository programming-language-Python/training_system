from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING, Type

from django.forms import ModelForm

from apps.testing.models.solving_tasks import SolvingOpenQuestion, SolvingClosedQuestion

if TYPE_CHECKING:
    from apps.testing.services import TestingService


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
    solving_task: SolvingOpenQuestion | SolvingClosedQuestion
