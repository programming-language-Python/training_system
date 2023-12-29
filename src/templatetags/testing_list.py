from django import template
from django.db.models import QuerySet

from apps.user.models import StudentGroup

register = template.Library()


@register.inclusion_tag('testing_list_buttons_tpl.html')
def show_testing_list_buttons(app_name: str, is_teacher: bool) -> dict[str, str]:
    testing_list_url = app_name + ":testing_list"
    if is_teacher:
        testing_create_url = app_name + ":testing_create"
    else:
        testing_create_url = ''
    return {
        'testing_list_url': testing_list_url,
        'testing_create_url': testing_create_url,
    }


@register.inclusion_tag('testing_list_tpl.html')
def show_testing_list(is_teacher: bool, testing_list: QuerySet) -> dict[str, bool | QuerySet]:
    return {
        'testing_list': testing_list,
        'is_teacher': is_teacher
    }


@register.inclusion_tag('student_groups_tpl.html')
def show_student_groups(student_groups: QuerySet[StudentGroup]) -> dict[str, QuerySet[StudentGroup]]:
    return {'student_groups': student_groups}


@register.inclusion_tag('testing_button_tpl.html')
def show_testing_button(absolute_url: str, is_teacher: bool) -> dict[str, str]:
    text = 'Настроить тестирование' if is_teacher else 'Пройти тест'
    return {
        'absolute_url': absolute_url,
        'text': text
    }
