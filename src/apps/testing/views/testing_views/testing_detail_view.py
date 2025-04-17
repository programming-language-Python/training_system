from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect


def redirect_testing_detail_view(request: WSGIRequest, testing_pk: int):
    if request.user.is_teacher():
        return redirect(f'testing:teacher_testing_detail', pk=testing_pk)
    return redirect(f'testing:student_testing_detail', testing_pk=testing_pk)
