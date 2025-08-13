from itertools import chain
from operator import attrgetter
from typing import Iterable

from django.db.models import Model

from apps.user.types import SortingTesting


def get_sorted_testings(sorting_testing: SortingTesting) -> Iterable[Model]:
    models = sorting_testing.models
    orm_filter = sorting_testing.orm_filter
    sorting_field = sorting_testing.sorting_field
    testings = [model.objects.filter(**orm_filter) for model in models]
    sorted_testings = sorted(
        chain(*testings),
        key=attrgetter(sorting_field),
        reverse=True,
    )
    return sorted_testings
