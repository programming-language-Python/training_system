from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from . import models


#
# class TestingInLineAdmin(admin.TabularInline):
#     model = models.Testing


# class TaskSetupInLineAdmin(admin.TabularInline):
#     model = models.TaskSetup


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id',)
    save_on_top = True


@admin.register(models.Testing)
class TestingAdmin(admin.ModelAdmin):
    # def setting(self, user) -> str:
    #     settings = []
    #     for setting in user.settings.all():
    #         settings.append(setting.name)
    #     return ' '.join(settings)
    #
    # setting.short_description = 'settings'

    # filter_vertical = [TaskSetupInLineAdmin]
    # inlines = [TaskSetupInLineAdmin]
    list_display = ('id', 'title')
    list_display_links = ('id',)
    search_fields = ('title',)
    list_editable = ('title',)
    list_filter = ('title',)
    save_on_top = True


@admin.register(models.TaskSetup)
class TaskSetupAdmin(admin.ModelAdmin):
    def testing(self, user) -> str:
        testings = []
        for testing in user.testings.all():
            testings.append(testing.name)
        return ' '.join(testings)

    testing.short_description = 'testings'
    # inlines = [TestingInLineAdmin]
    presence_one_of_cycles = {
        models.Cycle: {'widget': CheckboxSelectMultiple},
    }
    list_display = ('id', 'is_if_operator', 'condition_of_if_operator',
                    'cycle_condition')
    list_display_links = ('id',)
    list_filter = ('id', 'is_if_operator', 'condition_of_if_operator', 'presence_one_of_cycles',
                   'cycle_condition',
                   'operator_nesting')
    save_on_top = True

    class Media:
        js = ("js/admin/form_task_setup.js",)


@admin.register(models.Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('id', 'title')
    save_on_top = True


@admin.register(models.CompletedTesting)
class CompletedTestingAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment', 'total_weight', 'weight_of_student_tasks', 'tasks', 'testing', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('assessment', 'total_weight', 'weight_of_student_tasks', 'testing', 'student')
    list_filter = ('assessment', 'total_weight', 'weight_of_student_tasks', 'testing', 'student')
    save_on_top = True


admin.site.site_title = 'Управление тестированием'
admin.site.site_header = 'Управление тестированием'