from dataclasses import dataclass
from typing import Iterable, Type, Mapping

from django.db.models import Model


@dataclass
class SortingTesting:
    models: Iterable[Type[Model]]
    orm_filter: Mapping
    sorting_field: str
