from typing import Mapping

from django.contrib.auth.models import User
from django.db.models import F, Manager, QuerySet
from django.forms import Form

from testing.models import Task, Testing
from testing.services.setup_service import SetupService


class TaskService:
    user: User
    testing: Testing
    task: Manager[Task]
    task_form: Manager[Form]
    weight: int
    pk: int

    def __init__(self, user: User, forms: Mapping, testing: Testing) -> None:
        self.setup_service = SetupService(
            user=user,
            setup_form=forms['task_setup_form']
        )
        self.user = user
        self.testing = testing
        self.task = Task.objects
        self.task_form = forms['task_form']
        self.weight = self.task_form.cleaned_data['weight']

    def add(self) -> Manager[Task]:
        """Добавляет задачу Task"""
        self.setup_service.set()
        task_filter = self._filter()
        if task_filter.exists():
            self.task = self._increase_count(task=task_filter)
        else:
            self.task = self._create()
        return self.task

    def _filter(self) -> Manager[Task]:
        return self.task.filter(
            weight=self.weight,
            testing=self.testing,
            task_setup=self.setup_service.get_pk()
        )

    def _create(self) -> Manager:
        self.task = self.task.create(
            weight=self.weight,
            testing=self.testing,
            task_setup=self.setup_service.get(),
            count=1
        )
        return self.task

    def update(self, task) -> Task:
        is_changed_data = self.task_form.changed_data \
                          or self.setup_service.get_form().changed_data
        if is_changed_data:
            if task.count == 1:
                return self._update_non_recurring(task)
            return self._update_recurring(task)

    def _update_non_recurring(self, task: Task) -> Task:
        if self.task_form.changed_data \
                and self.setup_service.get_form().changed_data:
            self._update_weight(task)
            updated_task = self._update_if_setup_changed(task)
        elif self.task_form.changed_data:
            updated_task = self._update_weight(task)
        else:
            updated_task = self._update_if_setup_changed(task)
        return updated_task

    def _update_weight(self, task: Task) -> Task:
        task.weight = self.task_form.cleaned_data['weight']
        task.save(update_fields=['weight'])
        return task

    def _update_if_setup_changed(self, task: Task) -> Task:
        filtered_setup = self.setup_service.filter()
        if filtered_setup.exists():
            setup = filtered_setup.first()
            updated_task = self._set_update(task, setup)
        else:
            task.delete()
            updated_task = self.add()
        return updated_task

    def _set_update(self, task, setup) -> Manager[Task]:
        filtered_task = self._filter()
        if filtered_task.exists():
            task.delete()
            self.task = self._increase_count(task=filtered_task)
        else:
            self.task = self.setup_service.update(task, setup)
        return self.task

    def _update_recurring(self, task) -> Manager[Task]:
        _reduce_number_tasks(task)
        return self.add()

    def get_pk(self) -> int:
        is_manager = type(self.task) is Manager
        if is_manager:
            return self.task.first().pk
        return self.task.pk

    @staticmethod
    def _increase_count(task: QuerySet[Task] | Task) -> Manager[Task] | None:
        is_manager_task = type(task) is QuerySet[Task]
        if is_manager_task:
            task.update(count=F('count') + 1)
            return task.first()
        task.count += 1
        task.save(update_fields=['count'])


def delete(task: Task) -> None:
    if task.count > 1:
        _reduce_number_tasks(task)
    else:
        task.delete()


def _reduce_number_tasks(task: Task) -> None:
    task.count -= 1
    task.save(update_fields=['count'])
