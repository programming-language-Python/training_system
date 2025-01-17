from dataclasses import dataclass, fields
from datetime import datetime, time
from enum import Enum
from typing import Sequence, Type, TypeAlias, Iterable

from django.forms import ModelForm, inlineformset_factory

from apps.testing.constants import APP_NAME

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
class InlineFormSetFactory:
    form: ModelForm
    form_set: ModelForm | Type[inlineformset_factory]
    additional_form: ModelForm | None = None

    @property
    def forms(self) -> Iterable:
        forms = []
        for field in fields(self):
            field_value = getattr(self, field.name)
            if field_value:
                forms.append(field_value)
        return forms


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
