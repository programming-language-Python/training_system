from django.db.models import QuerySet, Q

from testing.models import Testing
from user.models import User


class FilterTesting:
    def __init__(self, user: User, query: QuerySet | None) -> None:
        self.user = user
        self.query = query

    def execute(self) -> QuerySet:
        is_teacher_ = self.user.is_teacher
        if is_teacher_:
            return self._get_for_teacher()
        return self._get_for_student()

    def _get_for_teacher(self) -> QuerySet:
        teacher_data = {'user': self.user}
        if self.query:
            search = Q(**teacher_data) & Q(title=self.query)
            return self._get_filter(search)
        return self._get_filter(teacher_data)

    def _get_for_student(self) -> QuerySet:
        student_data = {
            'is_published': True,
            'student_groups': self.user.student_group
        }
        if self.query:
            search = Q(**student_data) & Q(title=self.query)
            return self._get_filter(search)
        return self._get_filter(student_data)

    @staticmethod
    def _get_filter(query: Q | dict) -> QuerySet:
        if type(query) is dict:
            return Testing.objects.filter(**query)
        return Testing.objects.filter(query)
