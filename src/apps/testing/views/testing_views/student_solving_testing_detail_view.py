from typing import Mapping

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import redirect
from django.views.generic import ListView

from apps.testing.models import SolvingTask, Testing
from apps.testing.services import TestingService, TaskService
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
        solving_testing = self.testing_service.solving_testing
        context |= {
            'form': solving_task.task.service.get_solving_form(
                solving_testing_pk=solving_testing.pk,
            ),
            'end_passage': solving_testing.end_passage.strftime('%Y-%m-%dT%H:%M:%S'),
            'duration': solving_testing.duration.seconds,
            'testing': testing,
            'testing_title': testing.title,
            'quantity_task': testing.task_set.all().count(),
        }
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.testing_service = TestingService(
            testing_pk=self.kwargs['testing_pk'],
            student=self.request.user.student
        )
        is_time_up = self.testing_service.is_time_up()
        is_assessment = self.testing_service.get_solving_testing().assessment
        if is_time_up and not is_assessment:
            self._save_answer_task()
            return self.testing_service.end_testing()
        if is_assessment:
            return redirect('user:home')
        return super().dispatch(request, *args, **kwargs)

    def _save_answer_task(self) -> None:
        solving_task = self._get_solving_task()
        if solving_task.task.task_type == TaskType.OPEN_QUESTION:
            answer = self.request.POST.get('answer')
        else:
            answer = self.request.POST.getlist('answer')
        task_service = TaskService()
        task_service.save_answer(solving_task, answer)

    def _get_solving_task(self) -> SolvingTask:
        current_page = int(self.request.POST.get('current_page'))
        index_solving_task = current_page - 1
        return self.testing_service.start_testing()[index_solving_task]

    def get_queryset(self) -> QuerySet[SolvingTask]:
        return self.testing_service.start_testing()

    def post(self, request, *args, **kwargs) -> HttpResponse:
        self.object_list = self.get_queryset()
        self._save_answer_task()
        is_complete = bool(self.request.POST.get('complete'))
        if is_complete:
            return self.testing_service.end_testing()
        request = self._get_request_page(request)
        return super().get(request, *args, **kwargs)

    def _get_request_page(self, request: QueryDict) -> QueryDict:
        request_get = request.GET.copy()
        request_get['page'] = self.request.POST.get('page', '1')
        request.GET = request_get
        return request
