from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from . import models


class TestingInLineAdmin(admin.TabularInline):
    model = models.Testing


@admin.register(models.Testing)
class TestingAdmin(admin.ModelAdmin):
    def setting(self, user) -> str:
        settings = []
        for setting in user.settings.all():
            settings.append(setting.name)
        return ' '.join(settings)

    setting.short_description = 'settings'

    # filter_vertical = [TaskSettingInLineAdmin]
    list_display = ('id', 'title', 'setting')
    list_display_links = ('id',)
    search_fields = ('title', 'setting')
    list_editable = ('title', 'setting')
    list_filter = ('title', 'setting')
    save_on_top = True


@admin.register(models.TaskSetting)
class TaskSettingAdmin(admin.ModelAdmin):
    inlines = [TestingInLineAdmin]
    availability_of_cycles = {
        models.Cycle: {'widget': CheckboxSelectMultiple},
    }
    list_display = (
        'id', 'weight', 'is_if_operator', 'condition_of_if_operator',
        'cycle_condition')
    list_display_links = ('id',)
    list_filter = (
        'id', 'weight', 'is_if_operator', 'condition_of_if_operator', 'availability_of_cycles',
        'cycle_condition',
        'operator_nesting')
    save_on_top = True

    class Media:
        js = ("admin/js/form_task_setting_admin.js",)


@admin.register(models.Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('id', 'title')
    save_on_top = True


@admin.register(models.OperatorNesting)
class CycleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('id', 'title')
    save_on_top = True


@admin.register(models.CodeTemplate)
class CodeTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'setting')
    list_display_links = ('id',)
    search_fields = ('code', 'setting')
    list_editable = ('code', 'setting')
    list_filter = ('id', 'setting')
    save_on_top = True


@admin.register(models.CompletedTesting)
class CompletedTestingAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('student',)
    list_filter = ('student',)
    save_on_top = True


admin.site.site_title = 'Управление тестированием'
admin.site.site_header = 'Управление тестированием'
