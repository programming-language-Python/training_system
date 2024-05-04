from django.contrib import admin

from apps.testing.models import Testing, SolvingTesting
from apps.testing.models.solving_tasks import SolvingClosedQuestion, SolvingOpenQuestion
from apps.testing.models.task_answer_options import ClosedQuestionAnswerOption, OpenQuestionAnswerOption
from apps.testing.models.tasks import ClosedQuestion, OpenQuestion, TaskType

admin.site.register(Testing)
admin.site.register(TaskType)

admin.site.register(ClosedQuestion)
admin.site.register(ClosedQuestionAnswerOption)

admin.site.register(OpenQuestion)
admin.site.register(OpenQuestionAnswerOption)

admin.site.register(SolvingTesting)
admin.site.register(SolvingClosedQuestion)
admin.site.register(SolvingOpenQuestion)
