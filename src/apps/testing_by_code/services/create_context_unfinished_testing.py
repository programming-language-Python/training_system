import datetime
from typing import Mapping, Iterable

from apps.testing_by_code.models import Task, Testing
from apps.testing_by_code.services.generate_code.generate_java import GenerateJava
from apps.testing_by_code.types import Setting, ContextUnfinishedTesting
from apps.user.models import UnfinishedTesting, User


class CreateContextUnfinishedTesting:
    user: User
    testing: Testing
    tasks_context: dict
    number: int

    def __init__(self, user: User, testing: Testing) -> None:
        self.user = user
        self.testing = testing
        self.tasks_context = {}
        self.number = 1

    def execute(self) -> ContextUnfinishedTesting:
        tasks = self.testing.task_set.all()
        self._create_tasks(tasks)
        unfinished_testing = self._get_unfinished_testing(title=self.testing.title)
        return ContextUnfinishedTesting(
            testing=self.testing,
            start_passage=str(datetime.datetime.now()),
            task_data=unfinished_testing.tasks,
            tasks=tasks
        )

    def _create_tasks(self, tasks: Iterable) -> None:
        for task in tasks:
            self._create_task(task)
            self.number += 1

    def _create_task(self, task: Task) -> None:
        if task.count > 1:
            self._create_for_recurring_tasks(task)
        else:
            key = task.pk
            self._create_for_non_repetitive_tasks(key, task)

    def _create_for_recurring_tasks(self, task: Task) -> None:
        number_recurring_tasks = 1
        for i in range(task.count):
            key = str(task.pk) + '_' + str(number_recurring_tasks)
            self._create_for_non_repetitive_tasks(key, task)
            number_recurring_tasks += 1

    def _create_for_non_repetitive_tasks(self, key: str, task: Task) -> None:
        self.tasks_context[key] = self._get_task_data(task)

    def _get_task_data(self, task: Task) -> Mapping[str, str | int]:
        task_setting = task.setting
        setting = Setting(
            is_if_operator=task_setting.is_if_operator,
            condition_of_if_operator=task_setting.condition_of_if_operator,
            cycle=task_setting.cycle.all(),
            cycle_condition=task_setting.cycle_condition,
            operator_nesting=task_setting.operator_nesting.all(),
            is_OOP=task_setting.is_OOP,
            is_strings=task_setting.is_strings
        )
        generate_java = GenerateJava(setting=setting)
        task_data = {
            'number': self.number,
            'count': task.count,
            'weight': task.weight,
            'code': generate_java.execute(),
        }
        return task_data

    def _get_unfinished_testing(self, title: str) -> UnfinishedTesting:
        unfinished_testing, is_created = UnfinishedTesting.objects.get_or_create(
            title=title,
            student=self.user,
            defaults={'tasks': self.tasks_context}
        )
        return unfinished_testing
