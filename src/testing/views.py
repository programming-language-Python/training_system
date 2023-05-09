from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from testing.forms import TestingForm, TaskSetupForm, TaskForm
from testing.models import Testing, Task

from testing.services.create_completed_testing_service import CreateCompletedTestingService
from testing.services.decorators import is_teacher
from testing.services.generate_code.generate_java import GenerateJava
from testing.services.task_setup import TaskManager


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
                Q(is_published=True, student_groups=self.request.user.student_group) & Q(title=query)
            )
        return Testing.objects.filter(is_published=True, student_groups=self.request.user.student_group)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher = self.request.user.is_teacher
        context['card_footer_text'] = 'Настроить тестирование' if is_teacher else 'Пройти тест'
        return context


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing

    def __init__(self, **kwargs):
        super().__init__()
        self.context = ''
        self.tasks_context = {}
        self.task_setup_data = {}
        self.number = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        if not self.request.user.is_teacher:
            self.create_context(kwargs)
        return self.context

    def create_context(self, kwargs):
        testing = [value for value in kwargs.values()][0]
        tasks = testing.task_set.all()
        for task in tasks:
            task_setup = task.task_setup
            self.task_setup_data = {
                # 'use_of_all_variables': task_setup.use_of_all_variables,
                'is_if_operator': task_setup.is_if_operator,
                'condition_of_if_operator': task_setup.condition_of_if_operator,
                'presence_one_of_cycles': task_setup.presence_one_of_cycles.all(),
                'cycle_condition': task_setup.cycle_condition,
                'operator_nesting': task_setup.operator_nesting.all()
            }
            self.create_tasks_context(task)
            self.number += 1
        session_name = 'testing_' + str(testing.pk)
        self.create_session(session_name)
        self.context['task_data'] = self.request.session[session_name]
        # УДАЛИТЬ ПОТОМ!!!
        del self.request.session[session_name]
        self.context['tasks'] = tasks

    def create_tasks_context(self, task):
        if task.count > 1:
            self.create_context_for_recurring_tasks(task)
        else:
            self.create_task_context(task)

    def create_context_for_recurring_tasks(self, task):
        number_recurring_tasks = 1
        for i in range(task.count):
            randomizer_java = GenerateJava(**self.task_setup_data)
            task_data = {
                'number': self.number,
                'count': task.count,
                'weight': task.weight,
                'code': randomizer_java.get_code(),
            }
            key = str(task.pk) + '_' + str(number_recurring_tasks)
            self.tasks_context[key] = task_data
            number_recurring_tasks += 1

    def create_task_context(self, task):
        randomizer_java = GenerateJava(**self.task_setup_data)
        task_data = {
            'number': self.number,
            'count': task.count,
            'weight': task.weight,
            'code': randomizer_java.get_code(),
        }
        self.tasks_context[task.pk] = task_data

    def create_session(self, session_name):
        if not (session_name in self.request.session.keys()):
            self.request.session[session_name] = self.tasks_context

    @staticmethod
    def post(request, *args, **kwargs):
        testing = get_object_or_404(Testing, pk=kwargs['pk'])
        task_form = TaskForm(request.POST or None)
        task_setup_form = TaskSetupForm(request.POST or None)
        context = {
            'task_form': task_form,
            'task_setup_form': task_setup_form,
        }
        is_valid_forms = task_form.is_valid() and task_setup_form.is_valid()
        if is_valid_forms:
            task_manager = TaskManager(request.user, context, testing)
            task_manager.add()
            return redirect('testing:task_detail', pk=task_manager.pk)
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
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_setup = task.task_setup
    task_form = TaskForm(request.POST or None, instance=task)
    task_setup_form = TaskSetupForm(request.POST or None, instance=task_setup)
    context = {
        'task_form': task_form,
        'task_setup_form': task_setup_form,
        'task': task
    }
    if request.method == 'POST':
        is_valid_forms = task_form.is_valid() and task_setup_form.is_valid()
        if is_valid_forms:
            is_changed_data = task_form.changed_data or task_setup_form.changed_data
            if is_changed_data:
                context.pop('task')
                task_manager = TaskManager(request.user, context, task.testing)
                task_manager.update(task)
                return redirect('testing:task_detail', pk=task_manager.pk)
            change_number_of_tasks(task, '+')
            return redirect('testing:task_detail', pk=task.pk)
    return render(request, 'testing/task_form.html', context)


def change_number_of_tasks(task, operand):
    if operand == '+':
        task.count += 1
    elif operand == '-':
        task.count -= 1
    task.save(update_fields=['count'])


@login_required
@user_passes_test(is_teacher, login_url='testing:testing_detail', redirect_field_name=None)
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        if task.count > 1:
            change_number_of_tasks(task, '-')
        else:
            task.delete()
        return HttpResponse('')

    return HttpResponseNotAllowed(
        [
            'POST',
        ]
    )


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
    create_completed_testing_service = CreateCompletedTestingService(request)
    create_completed_testing_service.execute()
    return redirect('user:home')
