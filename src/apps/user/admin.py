from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(OrigUserAdmin):
    list_display = ('id', 'last_name', 'first_name', 'patronymic', 'username', 'email')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name', 'patronymic', 'username', 'email')
    list_filter = ('id', 'last_name', 'first_name', 'patronymic', 'username', 'email')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": ("last_name", "first_name", "patronymic", "email")
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
    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('id', 'name')
    save_on_top = True


admin.site.site_title = 'Управление пользователями'
admin.site.site_header = 'Управление пользователями'
