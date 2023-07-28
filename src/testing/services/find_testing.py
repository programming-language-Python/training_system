from django.db.models import QuerySet, Q

from user.models import User
from .filter_testing import FilterTesting
from ..models import CompletedTesting


def find_testings(user: User, title: str) -> QuerySet:
    filter_testing = FilterTesting(user)
    filtered_testing = filter_testing.execute()
    found_testing = filtered_testing.filter(title__contains=title)
    return found_testing


def find_completed_testings(user: User, query: str | int) -> QuerySet:
    q_obj = Q(student=user)
    if query.isdigit():
        q_obj &= Q(assessment=query)
    else:
        q_obj &= Q(title__contains=query)
    return CompletedTesting.objects.filter(q_obj)
