from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from typing import Sequence, Type, TypeAlias

from django.forms import ModelForm

from apps.testing.constants import APP_NAME
from custom_types import InlineFormSetFactory

Id: TypeAlias = int | str


class TaskType(str, Enum):
    CLOSED_QUESTION = 'Закрытый вопрос'
    OPEN_QUESTION = 'Открытый вопрос'
    SEQUENCING = 'Установление последовательности'

    @property
    def en_value(self) -> str:
        """Возвращает название типа на английском языке."""
        return self.name.lower()

    @property
    def url_to_create(self) -> str:
        """Возвращает URL для создания задачи данного типа."""
        return f'{APP_NAME}:task_{self.en_value}_create'

    @property
    def url_js(self) -> str:
        """Возвращает путь к JavaScript-файлу для данного типа."""
        return f'js/{self.en_value}.js'


@dataclass
class ValidTask:
    task_forms: InlineFormSetFactory
    type: TaskType
    testing_pk: int


@dataclass
class SolvingTestingData:
    task_forms: Sequence[Type[ModelForm]]
    task_form_data: Sequence['SolvingTaskEntity']


@dataclass
class SolvingTaskEntity:
    answer: str
    start_passage: datetime
    lead_time: time
    task: Id
    solving_testing: Id
