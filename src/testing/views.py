from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView

from testing.forms import TestingForm, SettingForm, TaskForm
from testing.models import Testing, Task

from testing.services.create_completed_testing import CreateCompletedTesting
from testing.services.create_context_for_student import CreateContextForStudent
from testing.services.decorators import is_teacher
from testing.services.filter_testing import FilterTesting
from testing.services.find_testing import find_testings
from testing.services.task_service import TaskService, delete, increase_count


class TestingCreateView(LoginRequiredMixin, CreateView):
    form_class = TestingForm
    template_name = 'testing/testing_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)


class TestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('search')
        if query:
            return find_testings(
                user=self.request.user,
                title=query
            )
        return self._get_filtered_testing()

    def _get_filtered_testing(self) -> QuerySet:
        user = self.request.user
        filter_testing = FilterTesting(user)
        return filter_testing.execute()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context['card_footer_text'] = 'Настроить тестирование'
        else:
            context['card_footer_text'] = 'Пройти тест'
        return context


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, str]:
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context = super().get_context_data(**kwargs)
        else:
            context = self._get_context_for_student(kwargs)
        return context

    def _get_context_for_student(self, kwargs) -> dict[str, str]:
        create_context_for_student = CreateContextForStudent(self.request)
        return create_context_for_student.execute(kwargs)

    @staticmethod
    def post(request, *args, **kwargs) -> None:
        task_form = TaskForm(request.POST or None)
        setting_form = SettingForm(request.POST or None)
        context = {
            'task_form': task_form,
            'setting_form': setting_form
        }
        is_valid_forms = task_form.is_valid() and setting_form.is_valid()
        if is_valid_forms:
            user = request.user
            forms = context
            testing = get_object_or_404(Testing, pk=kwargs['pk'])
            task_service = TaskService(user, forms, testing)
            task_service.add()
            return redirect('testing:task_detail', pk=task_service.get_pk())
        return render(request, 'testing/task_form.html', context)


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name_suffix = '_update'


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy('testing:testing_list')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'testing/inc/task/_detail.html'


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
        return redirect('testing:task_detail', pk=updated_task.pk)
    if not is_POST:
        return HttpResponseNotAllowed(['POST', ])
    if not is_changed_data:
        context['change_error'] = 'Данные не были изменены'
    context['task'] = task
    return render(request, 'testing/task_form.html', context)


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def duplicate_task(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    is_POST = request.method == 'POST'
    if is_POST:
        duplicated_task = increase_count(task)
        return redirect('testing:task_detail', pk=duplicated_task.pk)
    return HttpResponseNotAllowed(['POST', ])


@login_required
@user_passes_test(is_teacher, login_url='testing:testing_detail',
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
    return render(request, 'testing/task_form.html', context)


def create_completed_testing(request):
    create_completed_testing_ = CreateCompletedTesting(request)
    create_completed_testing_.execute()
    return redirect('user:home')
