from django.core.handlers.wsgi import WSGIRequest

from apps.testing.views.testing_views import TestingDetailTeacherView, TestingDetailStudentView


def show_testing_detail_view(request: WSGIRequest, pk: int):
    if request.user.is_teacher:
        return TestingDetailTeacherView.as_view()(request, pk=pk)
    else:
        return TestingDetailStudentView.as_view()(request, pk=pk)
