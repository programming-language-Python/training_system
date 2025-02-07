from typing import Mapping

from django.views.generic import TemplateView

from apps.user.models import Semester, Teacher, Discipline
from mixins import LoginMixin


class StudentTemplateView(LoginMixin, TemplateView):
    template_name = 'user/student_detail.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        filter_data = {'journal__student_group': self.request.user.student.student_group}
        semesters = Semester.objects.filter(**filter_data).distinct().order_by('-date_start')
        disciplines = Discipline.objects.filter(**filter_data).distinct()
        teachers = Teacher.objects.filter(**filter_data).distinct()
        journal_data = {
            'Семестры': {
                'model_name': 'semester',
                'objects': semesters
            },
            'Дисциплины': {
                'model_name': 'discipline',
                'objects': disciplines
            },
            'Преподаватели': {
                'model_name': 'teacher',
                'objects': teachers
            }
        }
        context |= {
            'journal_data': journal_data,
            'journal_url': 'user:student_journal'
        }
        return context
