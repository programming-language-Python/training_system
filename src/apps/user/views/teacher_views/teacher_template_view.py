from typing import Mapping

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.user.models import Semester, StudentGroup, Discipline, Student


class TeacherTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/teacher_detail.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        journal_data = {'journal__teacher__id': self.request.user.teacher.id}
        semesters = Semester.objects.filter(**journal_data).distinct().order_by('-date_start')
        student_groups = StudentGroup.objects.filter(**journal_data).distinct().order_by('-year_start_studying', 'name')
        disciplines = Discipline.objects.filter(**journal_data).distinct().order_by('name')
        students = Student.objects.filter(student_group__in=student_groups)
        journal_1_data = {
            'Семестры': {
                'model_name': 'semester',
                'objects': semesters
            },
            'Группы': {
                'model_name': 'student_group',
                'objects': student_groups
            },
            'Дисциплины': {
                'model_name': 'discipline',
                'objects': disciplines
            },
        }
        journal_2_data = journal_1_data | {
            'Студенты': {
                'model_name': 'student',
                'objects': students
            }
        }
        context |= {
            'journal_1_data': journal_1_data,
            'journal_2_data': journal_2_data,
            'testing_setting_journal_url': 'user:testing_setting_journal',
            'testing_result_journal_url': 'user:testing_result_journal'
        }
        return context
