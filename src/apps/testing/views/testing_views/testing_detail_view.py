from django.core.handlers.wsgi import WSGIRequest

from apps.testing.services import TestingService
from apps.testing.views.testing_views import TestingDetailTeacherView, TestingDetailStudentView


def show_testing_detail_view(request: WSGIRequest, pk: int):
    if request.user.is_teacher():
        return TestingDetailTeacherView.as_view()(request, pk=pk)
    else:
        student = request.user.student
        testing_service = TestingService(testing_pk=pk, student=student)
        solving_testing_data = testing_service.start_testing()
        return TestingDetailStudentView.as_view(
            testing_service=testing_service,
            form_list=solving_testing_data.task_forms,
            initial_dict=solving_testing_data.task_form_data
        )(request)
