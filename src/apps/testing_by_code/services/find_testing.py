from django.db.models import QuerySet, Q

from apps.user.models import Student, User
from .filter_testing import FilterTesting
from ..models import SolvingTesting


def find_testings(user: User, title: str) -> QuerySet:
    filter_testing = FilterTesting(user)
    filtered_testing = filter_testing.execute()
    found_testing = filtered_testing.filter(title__contains=title)
    return found_testing


def find_solved_testings(student: Student, query: str | int) -> QuerySet:
    q_obj = Q(student=student)
    if query.isdigit():
        q_obj &= Q(assessment=query)
    else:
        q_obj &= Q(title__contains=query)
    return SolvingTesting.objects.filter(q_obj)
