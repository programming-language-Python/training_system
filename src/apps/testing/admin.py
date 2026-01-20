from django.contrib import admin

from apps.testing.models import Testing, SolvingTesting, Task, SolvingTask
from apps.testing.models.task_answer_options import OpenQuestionAnswerOption, AnswerOption
from apps.testing.models.tasks import ClosedQuestion


@admin.register(SolvingTask)
class SolvingTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'solving_testing')
    list_filter = ('id', 'solving_testing')
    sortable_by = ('id', 'solving_testing')
    save_on_top = True


admin.site.register(Testing)
admin.site.register(Task)

admin.site.register(ClosedQuestion)

admin.site.register(AnswerOption)
admin.site.register(OpenQuestionAnswerOption)

admin.site.register(SolvingTesting)
