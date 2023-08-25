from django.db.models import QuerySet

from testing.models import Testing, CompletedTesting, Task
from user.models import User


class FilterTesting:
    def __init__(self, user: User) -> None:
        self.user = user

    def execute(self) -> QuerySet:
        if self.user.is_teacher:
            return self._get_for_teacher()
        return self._get_for_student()

    def _get_for_teacher(self) -> QuerySet:
        testing_info = {'user': self.user}
        return Testing.objects.filter(**testing_info)

    def _get_for_student(self) -> QuerySet:
        student_testing = self._get_non_empty_testings()
        completed_testing = CompletedTesting.objects.filter(
            testing__in=student_testing,
            student=self.user
        )
        if completed_testing.exists():
            titles_of_completed_tests = completed_testing.values_list('title', flat=True)
            student_testing = student_testing.exclude(title__in=titles_of_completed_tests)
        return student_testing

    def _get_non_empty_testings(self) -> QuerySet:
        testing_info = {
            'is_published': True,
            'student_groups': self.user.student_group
        }
        student_testing = Testing.objects.filter(**testing_info)
        student_testing_ids = student_testing.values_list('id', flat=True)
        ids_of_non_empty_testings = Task.objects.filter(
            testing__in=student_testing_ids,
            testing__isnull=False
        ).values_list('testing', flat=True)
        return Testing.objects.filter(id__in=ids_of_non_empty_testings)
