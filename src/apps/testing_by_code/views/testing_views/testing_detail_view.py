from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect


def redirect_testing_detail_view(request: WSGIRequest, pk: int):
    if request.user.is_teacher():
        return redirect(f'testing_by_code:teacher_testing_detail', pk=pk)
    return redirect(f'testing_by_code:student_testing_detail', pk=pk)
