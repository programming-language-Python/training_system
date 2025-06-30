from typing import Mapping

from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.testing_by_code.models import Testing, SolvingTesting
from apps.testing_by_code.services import TestingService
from apps.testing_by_code.constants import APP_NAME
from mixins import LoginMixin, ContextMixin


class StudentSolvingTestingDetailView(LoginMixin, ContextMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs) -> Mapping[str, SolvingTesting]:
        testing = kwargs['object']
        solving_testing = self._start_testing(testing)
        context = {
            'solving_testing': solving_testing,
            # 'end_passage': solving_testing.end_passage.strftime('%Y-%m-%dT%H:%M:%S'),
            # 'duration': solving_testing.duration.seconds,
        }
        return context

    def _start_testing(self, testing: Testing) -> SolvingTesting:
        testing_service = TestingService(
            student=self.request.user.student,
            testing=testing
        )
        return testing_service.start()

    @staticmethod
    def post(request, *args, **kwargs):
        post_method = request.POST
        solving_testing_pk = post_method.get('solving_testing_pk')
        user_answers = post_method.getlist('answer')
        solving_testing = SolvingTesting.objects.get(pk=solving_testing_pk)
        solving_testing.complete(user_answers)
        return redirect('user:home')
