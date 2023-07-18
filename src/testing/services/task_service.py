from typing import Mapping

from django.contrib.auth.models import User
from django.db.models import F, Manager
from django.forms import Form

from testing.models import Task, TaskSetup, Testing
from testing.services.filter_task_setup import FilterSetup


class TaskService:
    user: User
    testing: Testing
    task: Manager[Task]
    setup: Manager[TaskSetup]
    task_form: Manager[Form]
    weight: int
    setup_form: Manager[Form]
    setup_filter: Manager[FilterSetup]
    pk: int

    def __init__(self, user: User, forms: Mapping, testing: Testing) -> None:
        self.user = user
        self.testing = testing
        self.task = Task.objects
        self.setup = TaskSetup.objects
        self.task_form = forms['task_form']
        self.weight = self.task_form.cleaned_data['weight']
        self.setup_form = forms['setup_form']
        self.setup_filter = self._filter_setup()

    def _filter_setup(self) -> Manager[FilterSetup]:
        filter_task = FilterSetup(self.setup, self.setup_form)
        return filter_task.execute()

    def add(self) -> None:
        """Добавляет задачу Task"""
        self._set_setup()
        task_filter = self._get_filter()
        if task_filter.exists():
            task = _increase_count(task_filter)
            pk = task.first().pk
        else:
            task = self._create()
            pk = task.pk
        self._set_pk(pk)

    def _set_setup(self) -> None:
        if self.setup_filter.exists():
            setup = self.setup_filter.filter(users=self.user)
            if setup.exists():
                self.setup = setup.first()
            else:
                self.setup.first().users.add(self.user)
                self.setup = self.setup.first()
        else:
            self._create_setup()

    def _create_setup(self) -> None:
        self.setup = self.setup_form.save(commit=False)
        self.setup.pk = None
        self.setup.save()
        self.setup_form.save_m2m()
        self.setup.users.add(self.user)

    def _get_filter(self) -> Manager[Task]:
        return self.task.filter(
            weight=self.weight,
            testing=self.testing,
            setup=self.setup
        )

    def _set_pk(self, pk):
        self.pk = pk

    def _create(self) -> Manager:
        self.task = self.task.create(
            weight=self.weight,
            testing=self.testing,
            setup=self.setup,
            count=1
        )
        return self.task

    def update(self, task) -> None:
        if self.setup_form.changed_data:
            if task.count == 1:
                self._update_non_recurring(task)
            else:
                task.count -= 1
                task.save(update_fields=['count'])
                self.add()

    def _update_non_recurring(self, task) -> None:
        self._update_weight(task)
        if self.setup_filter.exists():
            self.setup = self.setup_filter.first()
            task_filter = self._get_filter()
            if task_filter.exists():
                task.delete()
                task = _increase_count(task=task_filter)
                pk = task.first().pk
            else:
                task = _update_setup(task, self.setup)
                pk = task.pk
            self._set_pk(pk)
        else:
            task.delete()
            self.add()

    def _update_weight(self, task) -> None:
        if self.task_form.changed_data:
            task.weight = self.task_form.cleaned_data['weight']
            task.save(update_fields=['weight'])

    def get_pk(self) -> int:
        return self.pk


def _update_setup(task: Manager, setup: Manager) -> Manager:
    task.setup = setup
    task.save(update_fields=['setup'])
    return task


def _increase_count(task: Manager) -> Manager:
    task.update(count=F('count') + 1)
    return task
