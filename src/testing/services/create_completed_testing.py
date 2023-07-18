from testing import models
from testing.services.run_code.run_java.run_java import RunJava
from testing.utils.utils import round_up


class CreateCompletedTesting:
    def __init__(self, request):
        self.request = request
        self.task_weights = [int(task_weight) for task_weight in request.GET.getlist('weight')]
        self.task_weight = ''
        self.user_answers = request.GET.getlist('answer')
        self.user_answer = ''
        self.codes = self.request.GET.getlist('code')
        self.code = ''
        self.weight_of_student_tasks = 0
        self.tasks = []

    def execute(self):
        self.add_tasks()
        models.CompletedTesting.objects.create(
            assessment=self.get_assessment(),
            total_weight=self.get_total_weight(),
            weight_of_student_tasks=self.weight_of_student_tasks,
            tasks=self.tasks,
            testing=self.get_testing(),
            student=self.request.user
        )
        # TODO Расскоментить?
        # self.delete_session()

    def add_tasks(self):
        for self.task_weight, self.user_answer, self.code in zip(self.task_weights, self.user_answers, self.codes):
            self.add_task()

    def add_task(self):
        run_java = RunJava(self.code)
        raw_answer = run_java.execute()
        answer = "".join(raw_answer.split())
        if answer == self.user_answer:
            self.weight_of_student_tasks += self.task_weight
        task = {
            'weight': self.task_weight,
            'code': self.code,
            'answer': answer,
            'user_answer': self.user_answer
        }
        self.tasks.append(task)

    def get_assessment(self):
        return round_up(self.weight_of_student_tasks / sum(self.task_weights) * 5)

    def get_total_weight(self):
        return sum(self.task_weights)

    def get_testing(self):
        return models.Testing.objects.get(pk=self.request.GET.get('testing_pk'))

    def delete_session(self):
        session_name = 'testing_' + str(self.request.GET.get('testing_pk'))
        del self.request.session[session_name]
