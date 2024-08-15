from typing import Type

from django.db.models import Q, QuerySet, Model


def find_solved_testings(solving_testing: Type[Model], student_pk: int, query: str | int) -> QuerySet:
    q_obj = Q(student=student_pk)
    if query.isdigit():
        q_obj &= Q(assessment=query)
    else:
        q_obj &= Q(testing__title__contains=query)
    return solving_testing.objects.filter(q_obj)
