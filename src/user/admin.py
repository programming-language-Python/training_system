from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(OrigUserAdmin):
    def student_group(self, user) -> str:
        groups_students = []
        for setting in user.user.groups.all():
            groups_students.append(setting.name)
        return ' '.join(groups_students)

    student_group.short_description = 'groups_students'
    list_display = ('id', 'last_name', 'first_name', 'patronymic', 'username', 'email', 'student_group', 'is_teacher')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name', 'patronymic', 'username', 'email')
    list_editable = ('student_group',)
    list_filter = ('id', 'last_name', 'first_name', 'patronymic', 'username', 'email', 'student_group')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": ("last_name", "first_name", "patronymic", "email", "is_teacher", "student_group")
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    save_on_top = True


@admin.register(models.StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id',)
    search_fields = ('id', 'title')
    list_editable = ('title',)
    list_filter = ('id', 'title')
    save_on_top = True


admin.site.site_title = 'Управление пользователями'
admin.site.site_header = 'Управление пользователями'
