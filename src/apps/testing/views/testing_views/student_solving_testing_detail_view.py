from typing import Mapping

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from apps.testing.models import SolvingTask, Testing
from apps.testing.services import TestingService
from apps.testing.types import TaskType
from mixins import LoginMixin


class StudentSolvingTestingDetailView(LoginMixin, ListView):
    model = SolvingTask
    template_name = 'testing/student_solving_testing_detail.html'
    context_object_name = 'solving_tasks'
    allow_empty = True
    paginate_by = 1

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        current_page = int(self.request.GET.get('page', 1))
        index_solving_task = current_page - 1
        solving_task = self.get_queryset()[index_solving_task]
        testing = Testing.objects.get(pk=self.kwargs['testing_pk'])
        context |= {
            'form': solving_task.task.service.get_solving_form(
                solving_testing_pk=self.testing_service.solving_testing.pk,
            ),
            'testing': testing,
            'quantity_task': testing.task_set.all().count(),
        }
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.testing_service = TestingService(
            testing_pk=self.kwargs['testing_pk'],
            student=self.request.user.student
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[SolvingTask]:
        return self.testing_service.start_testing()

    def post(self, request, *args, **kwargs) -> HttpResponse:
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        current_page = int(self.request.POST.get('current_page'))
        index_solving_task = current_page - 1
        solving_task = self.get_queryset()[index_solving_task]

        if solving_task.task.task_type == TaskType.OPEN_QUESTION:
            solving_task.answer = self.request.POST.get('answer')
        else:
            solving_task.answer = self.request.POST.getlist('answer')
        solving_task.save()

        is_last_page = int(self.request.POST.get('current_page')) == context['paginator'].num_pages
        if is_last_page:
            return self.testing_service.end_testing()

        request_get = request.GET.copy()
        request_get['page'] = self.request.POST.get('page', '1')
        request.GET = request_get
        return super().get(request, *args, **kwargs)
