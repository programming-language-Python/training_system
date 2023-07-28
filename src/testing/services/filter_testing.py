from django.db.models import QuerySet

from testing.models import Testing, CompletedTesting
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
        testing_info = {
            'is_published': True,
            'student_groups': self.user.student_group
        }
        student_testing = Testing.objects.filter(**testing_info)
        student_testing_values = student_testing.values()
        for testing in student_testing_values:
            is_was_testing = CompletedTesting.objects.filter(
                testing=testing['id'],
                student=self.user
            ).exists()
            if is_was_testing:
                student_testing = student_testing.exclude(id=testing['id'])
        return student_testing
