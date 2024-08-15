from typing import Mapping, Type

from django.db.models import QuerySet, Model
from django.views.generic import ListView

from apps.user.models import Student
from apps.user.services import find_solved_testings
from mixins import LoginMixin


class StudentSolvingTestingListMixin(LoginMixin, ListView):
    model: Type[Model]
    template_name = 'user/student_solving_testing_list.html'
    context_object_name = 'solving_testings'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        context['student_full_name'] = Student.objects.get(pk=self.kwargs['pk']).user.get_full_name()
        context['solving_task_list_template'] = f'{self.model._meta.app_label}/inc/solving_task/_solving_task_list.html'
        context['is_testing_by_code'] = True if self.model._meta.app_label == 'testing_by_code' else False
        return context

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('search')
        if query:
            return find_solved_testings(
                solving_testing=self.model,
                student_pk=self.kwargs['pk'],
                query=query
            )
        return self.model.objects.filter(student=self.kwargs['pk'])
