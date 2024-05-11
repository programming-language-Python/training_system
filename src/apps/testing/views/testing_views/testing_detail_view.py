from django.core.handlers.wsgi import WSGIRequest

from apps.testing.services import TestingService
from apps.testing.views.testing_views import TestingDetailTeacherView, TestingDetailStudentView


def show_testing_detail_view(request: WSGIRequest, pk: int):
    if request.user.is_teacher():
        return TestingDetailTeacherView.as_view()(request, pk=pk)
    else:
        testing_service = TestingService(testing_pk=pk)
        task_forms, form_task_data = testing_service.start_testing(
            student=request.user.student
        )
        form_task_data['testing_service'] = testing_service
        return TestingDetailStudentView.as_view(
            task_forms, initial_dict=form_task_data
        )(request)
