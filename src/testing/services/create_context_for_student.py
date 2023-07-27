import datetime
from typing import Mapping

from django.db.models import Manager

from testing.models import Task
from testing.services.generate_code.generate_java import GenerateJava
from testing.types import Setting


class CreateContextForStudent:
    setting: Setting
    context: dict[str, str]
    tasks_context: dict
    number: int

    def __init__(self, request) -> None:
        self.request = request
        self.context = {}
        self.tasks_context = {}
        self.number = 1

    def execute(self, kwargs: Mapping[str, Manager]) -> dict[str, str]:
        testing = [value for value in kwargs.values()][0]
        tasks = testing.task_set.all()
        for task in tasks:
            setting = task.setting
            self.setting = Setting(
                # 'use_of_all_variables': setting.use_of_all_variables,
                is_if_operator=setting.is_if_operator,
                condition_of_if_operator=setting.condition_of_if_operator,
                cycle=setting.cycle.all(),
                cycle_condition=setting.cycle_condition,
                operator_nesting=setting.operator_nesting.all(),
                is_OOP=setting.is_OOP,
                is_strings=setting.is_strings
            )
            self._create_tasks_context(task)
            self.number += 1
        session_name = 'testing_' + str(testing.pk)
        self._create_session(session_name)
        self.context['testing'] = testing
        self.context['start_passage'] = str(datetime.datetime.now())
        self.context['task_data'] = self.request.session[session_name]
        # TODO УДАЛИТЬ ПОТОМ!!!
        del self.request.session[session_name]
        self.context['tasks'] = tasks
        return self.context

    def _create_tasks_context(self, task: Task) -> None:
        if task.count > 1:
            self._create_context_for_recurring_tasks(task)
        else:
            # self._create_task_context(task)
            key = task.pk
            self._create_task_context(key, task)

    def _create_context_for_recurring_tasks(self, task: Task) -> None:
        number_recurring_tasks = 1
        for i in range(task.count):
            key = str(task.pk) + '_' + str(number_recurring_tasks)
            # self.tasks_context[key] = self._get_task_data(task)
            self._create_task_context(key, task)
            number_recurring_tasks += 1

    def _get_task_data(self, task: Task) -> Mapping[str, str | int]:
        generate_java = GenerateJava(setting=self.setting)
        task_data = {
            'number': self.number,
            'count': task.count,
            'weight': task.weight,
            'code': generate_java.execute(),
        }
        return task_data

    def _create_task_context(self, key: str, task: Task) -> None:
        self.tasks_context[key] = self._get_task_data(task)

    def _create_session(self, session_name: str) -> None:
        if not (session_name in self.request.session.keys()):
            self.request.session[session_name] = self.tasks_context
