from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, \
    UpdateView, DeleteView

from abstractions.abstract_views.abstarct_testing_create_view import AbstractTestingCreateView
from apps.testing_by_code.constants import APP_NAME
from apps.testing_by_code.forms import TestingForm, SettingForm, TaskForm
from apps.testing_by_code.models import Testing, Task, CompletedTesting

from apps.testing_by_code.services.create_completed_testing import CreateCompletedTesting
from apps.testing_by_code.services.create_context_unfinished_testing import CreateContextUnfinishedTesting
from apps.testing_by_code.services.decorators import is_teacher
from apps.testing_by_code.services.filter_testing import FilterTesting
from apps.testing_by_code.services.find_testing import find_testings
from apps.testing_by_code.services.task_service import TaskService, delete, increase_count
from mixins import URLMixin, ContextMixin


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        is_title_in_completed_testings = CompletedTesting.objects.filter(
            title=form.instance.title
        ).exists()
        if is_title_in_completed_testings:
            return self._add_error_title_exists(form)
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)


class TestingListView(ContextMixin, LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing
    template_name = 'testing_list.html'
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_list_data(is_teacher=self.request.user.is_teacher)
        return context

    def get_queryset(self) -> QuerySet[Testing]:
        query = self.request.GET.get('search')
        if query:
            return find_testings(
                user=self.request.user,
                title=query
            )
        return self._get_filtered_testing()

    def _get_filtered_testing(self) -> QuerySet[Testing]:
        user = self.request.user
        filter_testing = FilterTesting(user)
        return filter_testing.execute()


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, str]:
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context = super().get_context_data(**kwargs)
            context |= self.get_testing_detail_url_button_data()
        else:
            testing = kwargs['object']
            context = self._get_context_unfinished_testing(testing)
        return context

    def _get_context_unfinished_testing(self, testing: Testing) -> dict[str, str]:
        create_context_unfinished_testing = CreateContextUnfinishedTesting(
            user=self.request.user,
            testing=testing
        )
        return create_context_unfinished_testing.execute()

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
            return redirect('testing_by_code:task_detail', pk=task_service.get_pk())
        return render(request, 'testing_by_code/task_form.html', context)


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name = 'testing_update.html'


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy(APP_NAME + ':testing_list')
    template_name = 'testing_confirm_delete.html'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'testing_by_code/inc/task/_teacher_task_detail.html'


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


def create_completed_testing(request):
    create_completed_testing_ = CreateCompletedTesting(request)
    create_completed_testing_.execute()
    return redirect('user:home')
