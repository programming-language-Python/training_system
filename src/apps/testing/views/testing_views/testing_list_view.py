from django.db.models import QuerySet
from django.views.generic import ListView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from mixins import ContextMixin, LoginMixin


# TODO Этот класс дублируется
class TestingListView(LoginMixin, ContextMixin, ListView):
    model = Testing
    template_name = 'testing_list.html'
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_list_data(is_teacher=self.request.user.is_teacher())
        return context

    def get_queryset(self) -> QuerySet[Testing]:
        user = self.request.user
        if user.is_teacher():
            return Testing.objects.filter(teacher=user.teacher, date_of_deletion=None)
        else:
            return Testing.objects.filter(
                is_published=True,
                student_groups=user.student.student_group,
                testing_solving_testing_set__assessment__isnull=True
            )
