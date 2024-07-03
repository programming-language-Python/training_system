from django.contrib import admin

from .models import Task, Setting, Testing, Cycle, OperatorNesting, SolvingTesting, SolvingTask

admin.site.register(Testing)
admin.site.register(Task)
admin.site.register(Setting)
admin.site.register(Cycle)
admin.site.register(OperatorNesting)

admin.site.register(SolvingTesting)
admin.site.register(SolvingTask)

admin.site.site_title = 'Управление тестированием'
admin.site.site_header = 'Управление тестированием'
