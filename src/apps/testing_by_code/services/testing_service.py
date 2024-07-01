from typing import Mapping

from apps.testing_by_code.models import Task, Testing, SolvingTesting, SolvingTask
from apps.testing_by_code.services.generate_code.generate_java import GenerateJava
from apps.testing_by_code.services.run_code.run_java.run_java import RunJava
from apps.testing_by_code.types import Setting
from apps.user.models import Student


class TestingService:
    student: Student
    testing: Testing
    solving_testing: SolvingTesting

    def __init__(self, student: Student, testing: Testing) -> None:
        self.student = student
        self.testing = testing

    def start(self) -> Mapping[str, SolvingTesting]:
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing=self.testing,
            student=self.student,
        )
        if is_created:
            self._create_solving_tasks()

        return {
            'testing_title': self.testing.title,
            'solving_testing': self.solving_testing
        }

    def _create_solving_tasks(self) -> None:
        for task in self.testing.task_set.all():
            self._create_solving_task(task)

    def _create_solving_task(self, task: Task) -> None:
        if task.count > 1:
            self._create_for_recurring_tasks(task)
        else:
            self._create_for_non_repetitive_tasks(task)

    def _create_for_recurring_tasks(self, task: Task) -> None:
        for i in range(task.count):
            self._create_for_non_repetitive_tasks(task)

    def _create_for_non_repetitive_tasks(self, task: Task) -> None:
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
        code = generate_java.execute()
        run_java = RunJava(code)
        SolvingTask.objects.create(
            code=code,
            correct_answer=run_java.execute(),
            solving_testing=self.solving_testing,
            task=task
        )
