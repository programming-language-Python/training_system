from django.db.models import QuerySet

from apps.user.models import User
from .filter_testing import FilterTesting


def find_testings(user: User, title: str) -> QuerySet:
    filter_testing = FilterTesting(user)
    filtered_testing = filter_testing.execute()
    found_testing = filtered_testing.filter(title__contains=title)
    return found_testing
