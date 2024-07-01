from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from . import models
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

# @admin.register(models.Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('id', 'weight', 'testing', 'setting', 'count',)
#     save_on_top = True
#
#
# @admin.register(models.Testing)
# class TestingAdmin(admin.ModelAdmin):
#     # def setting(self, user) -> str:
#     #     settings = []
#     #     for setting in user.settings.all():
#     #         settings.append(setting.name)
#     #     return ' '.join(settings)
#     #
#     # setting.short_description = 'settings'
#
#     # filter_vertical = [SettingInLineAdmin]
#     # inlines = [SettingInLineAdmin]
#     list_display = ('id', 'title')
#     list_display_links = ('id',)
#     search_fields = ('title',)
#     list_editable = ('title',)
#     list_filter = ('title',)
#     save_on_top = True
#
#
# @admin.register(models.Setting)
# class SettingAdmin(admin.ModelAdmin):
#     def testing(self, user) -> str:
#         testings = []
#         for testing in user.testings.all():
#             testings.append(testing.name)
#         return ' '.join(testings)
#
#     testing.short_description = 'testings'
#     # inlines = [TestingInLineAdmin]
#     cycle = {
#         models.Cycle: {'widget': CheckboxSelectMultiple},
#     }
#     list_display = (
#         'id',
#         'is_if_operator',
#         'condition_of_if_operator',
#         'cycle_condition'
#     )
#     list_display_links = ('id',)
#     list_filter = (
#         'id',
#         'is_if_operator',
#         'condition_of_if_operator',
#         'cycle',
#         'cycle_condition',
#         'operator_nesting'
#     )
#     save_on_top = True
#
#
# @admin.register(models.Cycle)
# class CycleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title')
#     list_display_links = ('id', 'title')
#     search_fields = ('title',)
#     list_filter = ('id', 'title')
#     save_on_top = True
#
#
# @admin.register(models.OperatorNesting)
# class OperatorNestingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title')
#     list_display_links = ('id', 'title')
#     search_fields = ('title',)
#     list_filter = ('id', 'title')
#     save_on_top = True
#
#
# @admin.register(models.SolvingTesting)
# class SolvingTestingAdmin(admin.ModelAdmin):
#     fields_ = (
#         'assessment',
#         'total_weight',
#         'weight_of_student_tasks',
#         'start_passage',
#         'end_passage',
#         'student'
#     )
#     readonly_fields = ('start_passage', 'end_passage',)
#     list_display = ('id',) + fields_
#     list_display_links = ('id', 'student')
#     search_fields = fields_
#     list_filter = fields_
#     save_on_top = True
