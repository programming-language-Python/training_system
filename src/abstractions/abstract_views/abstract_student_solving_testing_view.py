from abc import ABC, abstractmethod
from typing import Mapping, Type
from django.db.models import QuerySet, Model
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from mixins import LoginMixin


class AbstractStudentSolvingTestingDetailView(LoginMixin, ListView, ABC):
    model = None
    template_name = None
    context_object_name = 'solving_tasks'
    allow_empty = True
    paginate_by = 1

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.testing_service = None

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self._initialize_service(
            testing_pk=self.kwargs['pk'],
            student_pk=request.user.student.pk
        )
        self.testing_service.start_testing()

        is_time_up = self.testing_service.is_time_up()
        is_assessment = self.testing_service.get_solving_testing().assessment
        is_end_testing = is_time_up and not is_assessment
        if is_end_testing:
            current_page = request.GET.get('page')
            if current_page:
                solving_task = self._get_current_solving_task(current_page)
                self._save_answer(request, solving_task)
            return self.testing_service.end_testing()
        if is_assessment:
            return redirect('user:home')
        return super().dispatch(request, *args, **kwargs)

    @abstractmethod
    def _initialize_service(self, testing_pk: int, student_pk: int) -> None:
        pass

    @staticmethod
    @abstractmethod
    def _save_answer(request: HttpRequest, solving_task) -> None:
        pass

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)

        current_page = int(self.request.GET.get('page', 1))
        current_solving_task = self._get_current_solving_task(current_page)
        solving_testing = self.testing_service.get_solving_testing()
        testing = solving_testing.testing

        form = self._get_initialized_solving_task_form(solving_task=current_solving_task)
        context |= {
            'form': form,
            'testing': testing,
            'quantity_task': testing.task_set.count(),
        }
        if testing.lead_time:
            context |= {
                'end_passage': solving_testing.end_passage.strftime('%Y-%m-%dT%H:%M:%S'),
                'duration': solving_testing.duration.seconds,
            }
        return context

    @abstractmethod
    def _get_initialized_solving_task_form(self, solving_task: Type[Model]) -> Type[ModelForm]:
        pass

    def _get_current_solving_task(self, current_page: int) -> Type[Model]:
        index_solving_task = current_page - 1
        return self.get_queryset()[index_solving_task]

    def get_queryset(self) -> QuerySet:
        return self.testing_service.solving_tasks.select_related('task')

    def post(self, request, *args, **kwargs) -> HttpResponse:
        current_page = int(request.POST.get('current_page', 1))
        self._save_answer(request, self._get_current_solving_task(current_page))
        if bool(request.POST.get('complete')):
            return self.testing_service.end_testing()
        request = self._update_request_page(request)
        return super().get(request, *args, **kwargs)

    def _update_request_page(self, request: HttpRequest) -> HttpRequest:
        request_get = request.GET.copy()
        request_get['page'] = self.request.POST.get('page', '1')
        request.GET = request_get
        return request
