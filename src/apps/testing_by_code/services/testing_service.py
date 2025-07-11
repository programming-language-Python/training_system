from django.db.models import Sum, F

from abstractions.abstract_services import AbstractTestingService
from apps.testing_by_code.models import Task, SolvingTesting, SolvingTask
from apps.testing_by_code.services.generate_code.generate_java import GenerateJava
from apps.testing_by_code.services.run_code.run_java.run_java import RunJava
from apps.testing_by_code.types import Setting
from utils import round_up


class TestingService(AbstractTestingService):
    def _get_or_create_solving_testing(self) -> tuple[SolvingTesting, bool]:
        return SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student_id=self.student_pk,
        )

    def _create_solving_task(self, task: Task) -> None:
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

    def _calculate_assessment(self) -> int:
        earned_weight = self._calculate_earned_weight()
        testing = self.solving_testing.testing
        assessment = round_up(earned_weight / testing.get_total_weight() * 5)
        self.solving_testing.earned_weight = earned_weight
        return assessment

    def _calculate_earned_weight(self) -> int:
        return self.solving_testing.solving_task_set.select_related('task').filter(
            answer=F('correct_answer')
        ).aggregate(
            Sum('task__weight')
        )['task__weight__sum'] or 0
