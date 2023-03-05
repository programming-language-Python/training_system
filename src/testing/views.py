from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from testing.forms import TestingForm, TaskSetupForm, TaskForm
from testing.models import Testing, Task, CompletedTesting
from testing.services.code_conversion import JavaToPythonConversion
from testing.services.code_generation import RandomizerJava
from testing.services.decorators import is_teacher
from testing.services.task_setup import TaskManager


# Create your views here.
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
        if self.request.user.is_teacher:
            return Testing.objects.filter(user=self.request.user)
        return Testing.objects.filter(is_published=True, student_groups=self.request.user.student_group)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher = self.request.user.is_teacher
        context['card_footer_text'] = 'Настроить тестирование' if is_teacher else 'Пройти тест'
        return context


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_teacher:
            testing = [value for value in kwargs.values()][0]
            tasks = testing.task_set.all()
            tasks_context = {}
            number = 1
            for task in tasks:
                task_setup = task.task_setup
                task_setup = {
                    'use_of_all_variables': task_setup.use_of_all_variables,
                    'is_if_operator': task_setup.is_if_operator,
                    'condition_of_if_operator': task_setup.condition_of_if_operator,
                    'presence_one_of_cycles': task_setup.presence_one_of_cycles.all(),
                    'cycle_condition': task_setup.cycle_condition,
                    'operator_nesting': task_setup.operator_nesting.all()
                }
                if task.count > 1:
                    number_recurring_tasks = 1
                    for i in range(task.count):
                        randomizer_java = RandomizerJava(**task_setup)
                        task_data = {
                            'number': number,
                            'count': task.count,
                            'weight': task.weight,
                            'code': randomizer_java.generate_code(),
                        }
                        key = str(task.pk) + '_' + str(number_recurring_tasks)
                        tasks_context[key] = task_data
                        number_recurring_tasks += 1
                        number += 1
                else:
                    randomizer_java = RandomizerJava(**task_setup)
                    task_data = {
                        'number': number,
                        'count': task.count,
                        'weight': task.weight,
                        'code': randomizer_java.generate_code(),
                    }
                    tasks_context[task.pk] = task_data
                    number += 1

            session_name = 'testing_' + str(testing.pk)
            if not (session_name in self.request.session.keys()):
                self.request.session[session_name] = tasks_context
            context['task_data'] = self.request.session[session_name]
            context['tasks'] = tasks
            # !!! УБРАТЬ ЕЁ ПОТОМ !!!
            del self.request.session[session_name]
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
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
    # fields = ['title', 'student_groups', 'is_published']
    template_name_suffix = '_update'


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy('testing:testing_list')


# @login_required
# @user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
# def testing_delete(request, pk):
#     task_setup = get_object_or_404(Testing, id=pk)
#
#     if request.method == 'POST':
#         task_setup.delete()
#         return redirect('testing:testing_list')
#
#     return HttpResponseNotAllowed(
#         [
#             'POST',
#         ]
#     )


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def update_testing(request, id_of_one_test):
    testing = get_object_or_404(Testing, id=id_of_one_test)
    form = TestingForm(request.POST or None, instance=testing)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('testing:create_task_setup', pk=testing.id)

    context = {
        'testing': testing,
        'form': form
    }
    return render(request, 'inc/testing/_form.html', context)


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


# class CreateTaskForm(CreateView):
#     form_class = TaskSetupForm
#     template_name = 'testing/task_form.html'


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


def create_completed_test(request):
    task_weight_list = [int(task_weight) for task_weight in request.GET.getlist('weight')]
    list_user_answers = request.GET.getlist('answer')
    code_list = request.GET.getlist('code')
    weight_of_student_tasks = 0
    tasks = []
    for task_weight, user_answer, code in zip(task_weight_list, list_user_answers, code_list):
        java_to_python_conversion = JavaToPythonConversion(code)
        answer = int(java_to_python_conversion.run_code())
        if answer == int(user_answer):
            weight_of_student_tasks += task_weight
        task = {
            'weight': task_weight,
            'code': code,
            'answer': answer,
            'user_answer': user_answer
        }
        tasks.append(task)
    assessment = round_up(weight_of_student_tasks / sum(task_weight_list) * 5)
    testing = Testing.objects.get(pk=request.GET.get('testing_pk'))
    CompletedTesting.objects.create(assessment=assessment,
                                    total_weight=sum(task_weight_list),
                                    weight_of_student_tasks=weight_of_student_tasks,
                                    tasks=tasks,
                                    testing=testing,
                                    student=request.user)
    # РАССКОМЕНТИТЬ ПОТОМ !!!
    # session_name = request.GET.get('testing_pk')
    # del request.session[session_name]
    return redirect('user:home')


def round_up(num):
    return int(num + (0.5 if num > 0 else -0.5))
