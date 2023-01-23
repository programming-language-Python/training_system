from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from testing.forms import TestingForm, TaskSetupForm
from testing.models import Testing, TaskSetup
from testing.services.decorators import is_teacher
from testing.services.task_setup import Task


# Create your views here.
class TestingList(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing
    queryset = model.objects.all().distinct('id_of_one_test')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher = self.request.user.is_teacher
        context['card_footer_text'] = 'Настроить тестирование' if is_teacher else 'Пройти тест'
        return context


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def create_testing(request):
    testing_form = TestingForm(request.POST or None)

    if request.method == 'POST':
        if testing_form.is_valid():
            user = request.user
            '''Сделать проверку на создание task setting'''
            task_setup = TaskSetup.objects.create()

            testing = testing_form.save(commit=False)
            testing.user = user
            testing.task_setup = task_setup
            testing.save()
            testing_form.save_m2m()
            task_setup.user.add(user)
            testing.id_of_one_test = testing.id
            testing.save()
            return redirect(testing)

    context = {
        'testing_form': testing_form
    }
    return render(request, 'testing/create_testing.html', context)


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


@login_required
# @user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def create_task_setup(request, id_of_one_test):
    # testing = get_object_or_404(Testing, id_of_one_test=id_of_one_test)
    testing = Testing.objects.filter(id_of_one_test=id_of_one_test)
    task_setups = TaskSetup.objects.filter(testing__in=testing)
    # task_setups = testing.select_related('task_setup').all()
    form = TaskSetupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # print(form.values('id_of_one_test').distinct())
            task = Task(request.user, form, testing.first())
            task.add()
            # obj, created = filtered_many_to_many_relationship.filter(user=request.user).get_or_create(
            #     **form.cleaned_data,
            #     user=request.user
            # )
            # print(obj, created)

            # saved_form_task_setup = form.save(commit=False)
            # user = request.user
            # saved_form_task_setup.user = user
            # saved_form_task_setup.save()
            # form.save_m2m()
            #
            #
            #
            # created_testing = Testing.objects.create(title=testing.title,
            #                                          id_of_one_test=testing.id_of_one_test,
            #                                          task_setup=saved_form_task_setup,
            #                                          user=user
            #                                          )
            # for student_group in testing.student_group.all():
            #     created_testing.student_group.add(student_group)
            # return redirect('testing:task_setup_detail', pk=saved_form_task_setup.id)
            return redirect('testing:task_setup_detail', pk=task.task_setup_id)
        else:
            return render(request, 'inc/task_setup/_form.html', context={
                'form': form
            })

    context = {
        'form': form,
        'testing': testing.first(),
        'task_setups': task_setups
    }
    return render(request, 'testing/testing_detail.html', context)


@login_required
def task_setup_detail(request, pk):
    task_setup = get_object_or_404(TaskSetup, id=pk)

    context = {
        'task_setup': task_setup
    }
    return render(request, 'testing/inc/task_setup/_detail.html', context)


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def update_task_setup(request, pk):
    task_setup = get_object_or_404(TaskSetup, id=pk)
    form = TaskSetupForm(request.POST or None, instance=task_setup)

    # testing = Testing.objects.filter(id_of_one_test=id_of_one_test)
    # task_setups = TaskSetup.objects.filter(testing__in=testing)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('testing:task_setup_detail', pk=task_setup.id)

    context = {
        'form': form,
        'task_setup': task_setup
    }
    return render(request, 'inc/task_setup/_form.html', context)


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def delete_task_setup(request, pk):
    task_setup = get_object_or_404(TaskSetup, id=pk)

    if request.method == 'POST':
        task_setup.delete()
        return HttpResponse('')

    return HttpResponseNotAllowed(
        [
            'POST',
        ]
    )


@login_required
@user_passes_test(is_teacher, login_url='user:home', redirect_field_name=None)
def add_task_setup_form(request):
    form = TaskSetupForm()

    context = {
        'form': form,
    }
    return render(request, 'inc/task_setup/_form.html', context)
