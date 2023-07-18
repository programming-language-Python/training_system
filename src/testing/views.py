from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView

from testing.forms import TestingForm, TaskSetupForm, TaskForm
from testing.models import Testing, Task

from testing.services.create_completed_testing import CreateCompletedTesting
from testing.services.create_context_for_student import CreateContextForStudent
from testing.services.decorators import is_teacher
from testing.services.task_service import TaskService


class TestingCreateView(LoginRequiredMixin, CreateView):
    form_class = TestingForm
    template_name = 'testing/testing_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)


class TestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing

    def get_queryset(self):
        query = self.request.GET.get('search')
        if self.request.user.is_teacher:
            if query:
                return Testing.objects.filter(
                    Q(user=self.request.user) & Q(title=query)
                )
            return Testing.objects.filter(user=self.request.user)
        if query:
            return Testing.objects.filter(
                Q(
                    is_published=True,
                    student_groups=self.request.user.student_group
                )
                & Q(title=query)
            )
        return Testing.objects.filter(
            is_published=True,
            student_groups=self.request.user.student_group
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher
        context[
            'card_footer_text'
        ] = 'Настроить тестирование' if is_teacher_ else 'Пройти тест'
        return context


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, str]:
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context = super().get_context_data(**kwargs)
        else:
            context = self._create_context_for_student(kwargs)
        return context

    def _create_context_for_student(self, kwargs) -> dict[str, str]:
        create_context_for_student = CreateContextForStudent(self.request)
        return create_context_for_student.execute(kwargs)

    @staticmethod
    def post(request, *args, **kwargs) -> None:
        testing = get_object_or_404(Testing, pk=kwargs['pk'])
        task_form = TaskForm(request.POST or None)
        task_setup_form = TaskSetupForm(request.POST or None)
        context = {
            'task_form': task_form,
            'task_setup_form': task_setup_form,
        }
        is_valid_forms = task_form.is_valid() and task_setup_form.is_valid()
        if is_valid_forms:
            task_service = TaskService(
                user=request.user,
                forms=context,
                testing=testing
            )
            task_service.add()
            return redirect('testing:task_detail', pk=task_service.get_pk())
        return render(request, 'testing/task_form.html', context=context)


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
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_setup = task.task_setup
    task_form = TaskForm(request.POST or None, instance=task)
    task_setup_form = TaskSetupForm(request.POST or None, instance=task_setup)
    context = {
        'task': task,
        'task_form': task_form,
        'task_setup_form': task_setup_form
    }
    is_POST = request.method == 'POST'
    is_valid_forms = task_form.is_valid() and task_setup_form.is_valid()
    if is_POST and is_valid_forms:
        is_changed_data = task_form.changed_data or task_setup_form.changed_data
        if is_changed_data:
            context.pop('task')
            task_service = TaskService(
                user=request.user,
                forms=context,
                testing=task.testing
            )
            task_service.update(task)
            return redirect('testing:task_detail', pk=task_service.get_pk())
        _increase_number_tasks(task)
        return redirect('testing:task_detail', pk=pk)
    return render(request, 'testing/task_form.html', context)


def _increase_number_tasks(task: Task) -> None:
    task.count += 1
    task.save(update_fields=['count'])


@login_required
@user_passes_test(is_teacher, login_url='testing:testing_detail',
                  redirect_field_name=None)
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    is_POST = request.method == 'POST'
    if is_POST:
        if task.count > 1:
            _reduce_number_tasks(task)
        else:
            task.delete()
        return HttpResponse('')
    return HttpResponseNotAllowed(['POST', ])


def _reduce_number_tasks(task) -> None:
    task.count -= 1
    task.save(update_fields=['count'])


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def add_task_form(request):
    task_form = TaskForm()
    task_setup_form = TaskSetupForm()
    context = {
        'task_form': task_form,
        'task_setup_form': task_setup_form,
    }
    return render(request, 'testing/task_form.html', context)


def create_completed_testing(request):
    create_completed_testing_service = CreateCompletedTesting(request)
    create_completed_testing_service.execute()
    return redirect('user:home')
