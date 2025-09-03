from typing import Mapping

from django.contrib.auth.models import User
from django.db.models import Manager
from django.forms import Form

from apps.testing_by_code.models import Task, Testing

from apps.testing_by_code.services import SettingService


class TaskService:
    user: User
    testing: Testing
    task: Manager[Task]
    task_form: Manager[Form]
    weight: int
    pk: int

    def __init__(self, user: User, forms: Mapping, testing: Testing) -> None:
        self.setting_service = SettingService(
            setting_form=forms['setting_form']
        )
        self.user = user
        self.testing = testing
        self.task = Task.objects
        self.task_form = forms['task_form']
        self.weight = self.task_form.cleaned_data['weight']

        self.setting_form = forms['setting_form']

    def create(self) -> Manager[Task]:
        self.setting_service.set()
        task_form = self.task_form.save(commit=False)
        task_form.serial_number = self.testing.task_set.count() + 1
        task_form.testing = self.testing
        task_form.setting = self.setting_service.get()
        task_form.save()
        self.task = task_form
        return self.task

    def update(self) -> Task:
        is_changed_data_setting_form = self.setting_service.get_form().changed_data
        task = self.task_form.save()
        if is_changed_data_setting_form:
            task = self._update_if_setting_changed(task)
        return task

    def _update_weight(self, task: Task) -> Task:
        task.weight = self.task_form.cleaned_data['weight']
        task.save(update_fields=['weight'])
        return task

    def _update_if_setting_changed(self, task: Task) -> Task:
        filtered_setting = self.setting_service.filter()
        if filtered_setting.exists():
            setting = filtered_setting.first()
            self.task = self.setting_service.update(task, setting)
        else:
            task.delete()
            self.create()
        return self.task

    @property
    def pk(self) -> int:
        is_manager = type(self.task) is Manager
        if is_manager:
            return self.task.first().pk
        return self.task.pk
