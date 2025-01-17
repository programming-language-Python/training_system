from apps.testing.models import Task, SolvingTask


def open_question_set_answer(solving_task: SolvingTask, answer: str) -> None:
    solving_task.answer = answer
    solving_task.save()


class OpenQuestionService:
    task: Task

    def __init__(self, task: Task):
        self.task = task

    def get_weight(self, answer: str) -> int:
        is_correct_answer = self.task.open_question_answer_option_set.filter(
            correct_answer=answer
        ).exists()
        return 1 if is_correct_answer else 0
