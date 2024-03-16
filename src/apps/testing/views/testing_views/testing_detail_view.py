from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerForm
from apps.testing.models.tasks import OpenQuestion
from apps.testing.services import TaskService
from apps.testing.views.testing_views import TestingDetailTeacherView, TestingDetailStudentView


def show_testing_detail_view(request: WSGIRequest, pk: int):
    if request.user.is_teacher:
        return TestingDetailTeacherView.as_view()(request, pk=pk)
    else:
        task_service = TaskService(testing_pk=pk)
        tasks = task_service.sort_tasks_serial_number()
        form_data = {}
        task_forms = []
        for page, task in enumerate(tasks):
            form_data[page] = {}
            if isinstance(task, OpenQuestion):
                task_forms.append(OpenQuestionAnswerForm)
                form_data[page]['task_pk'] = task.pk
                form_data[page]['serial_number'] = task.serial_number
                form_data[page]['description'] = mark_safe(task.description)
        return TestingDetailStudentView.as_view(task_forms, initial_dict=form_data)(request, pk=pk)
