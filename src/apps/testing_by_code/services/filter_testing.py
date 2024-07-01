from django.db.models import QuerySet

from apps.testing_by_code.models import Testing
from apps.user.models import User


class FilterTesting:
    def __init__(self, user: User) -> None:
        self.user = user

    def execute(self) -> QuerySet[Testing]:
        if self.user.is_teacher():
            return self._get_for_teacher()
        return self._get_for_student()

    def _get_for_teacher(self) -> QuerySet[Testing]:
        return Testing.objects.filter(teacher__user=self.user)

    def _get_for_student(self) -> QuerySet[Testing]:
        return Testing.objects.filter(
            is_published=True,
            student_groups=self.user.student.student_group,
            task_set__isnull=False,
            testing_by_code_solving_testing_set__end_passage__isnull=True
        ).distinct()
