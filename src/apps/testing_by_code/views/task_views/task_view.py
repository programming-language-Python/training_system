from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.testing_by_code.forms import SettingForm, TaskForm
from apps.testing_by_code.models import Task

from apps.testing_by_code.services.decorators import is_teacher
from apps.testing_by_code.services.task_service import TaskService, delete, increase_count


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def update_task(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    task_form = TaskForm(request.POST or None, instance=task)
    setting = task.setting
    setting_form = SettingForm(request.POST or None, instance=setting)
    context = {
        'task_form': task_form,
        'setting_form': setting_form,
    }
    is_POST = request.method == 'POST'
    is_valid_forms = task_form.is_valid() and setting_form.is_valid()
    is_changed_data = task_form.changed_data or setting_form.changed_data
    is_valid = is_POST and is_valid_forms and is_changed_data
    if is_valid:
        user = request.user
        forms = context
        testing = task.testing
        task_service = TaskService(user, forms, testing)
        updated_task = task_service.update(task)
        return redirect('testing_by_code:task_detail', pk=updated_task.pk)
    if not is_POST:
        return HttpResponseNotAllowed(['POST', ])
    if not is_changed_data:
        context['change_error'] = 'Данные не были изменены'
    context['task'] = task
    return render(request, 'testing_by_code/task_form.html', context)


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def duplicate_task(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    is_POST = request.method == 'POST'
    if is_POST:
        duplicated_task = increase_count(task)
        return redirect('testing_by_code:task_detail', pk=duplicated_task.pk)
    return HttpResponseNotAllowed(['POST', ])


@login_required
@user_passes_test(is_teacher, login_url='testing_by_code:testing_detail',
                  redirect_field_name=None)
def delete_task(request, pk: int):
    is_POST = request.method == 'POST'
    if is_POST:
        task = get_object_or_404(Task, id=pk)
        delete(task)
        return HttpResponse('')
    return HttpResponseNotAllowed(['POST', ])


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def add_task_form(request):
    task_form = TaskForm()
    setting_form = SettingForm()
    context = {
        'task_form': task_form,
        'setting_form': setting_form,
    }
    return render(request, 'testing_by_code/task_form.html', context)
