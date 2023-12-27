from typing import Protocol

from django.db.models import QuerySet


class IFilterTesting(Protocol):
    def get_non_empty_testings(self) -> QuerySet:
        raise NotImplementedError
