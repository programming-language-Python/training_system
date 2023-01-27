from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from testing.forms import TestingForm, TaskSetupForm
from testing.models import Testing, TaskSetup, Task
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
        return Testing.objects.filter(student_group=self.request.user.student_group)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher = self.request.user.is_teacher
        context['card_footer_text'] = 'Настроить тестирование' if is_teacher else 'Пройти тест'
        return context


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            testing = get_object_or_404(Testing, pk=kwargs['pk'])
            form = TaskSetupForm(request.POST or None)
            if form.is_valid():
                task = TaskManager(request.user, form, testing)
                task.add()
                return redirect('testing:task_detail', pk=task.id)
            return render(request, 'testing/task_form.html', context={
                'form': form
            })


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    fields = ['title', 'student_group', 'is_published']
    template_name_suffix = '_update'


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def testing_delete(request, pk):
    task_setup = get_object_or_404(Testing, id=pk)

    if request.method == 'POST':
        task_setup.delete()
        return redirect('testing:testing_list')

    return HttpResponseNotAllowed(
        [
            'POST',
        ]
    )


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
    form = TaskSetupForm(request.POST or None, instance=task_setup)

    if request.method == 'POST':
        if form.is_valid():
            if form.changed_data:
                # testing = task.testing
                task_manager = TaskManager(request.user, form)
                task_manager.update(task)
                return redirect('testing:task_detail', pk=task_manager.id)
            else:
                change_number_of_tasks(task, '+')
                return redirect('testing:task_detail', pk=task.pk)

    context = {
        'form': form,
        'task': task,
        'task_setup': task_setup
    }
    return render(request, 'testing/task_form.html', context)


def change_number_of_tasks(task, operand):
    if operand == '+':
        task.count += 1
        task.save(update_fields=['count'])
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
    form = TaskSetupForm()

    context = {
        'form': form,
    }
    return render(request, 'testing/task_form.html', context)
