import json
from typing import Mapping, Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from apps.user.models import User, Semester, StudentGroup, Discipline, Journal


class TeacherTemplateView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        journal_data = {'journal__teacher__id': self.request.user.teacher.id}
        semesters = Semester.objects.filter(**journal_data).distinct().order_by('-date_start')
        student_groups = StudentGroup.objects.filter(**journal_data).distinct().order_by('-year_start_studying', 'name')
        disciplines = Discipline.objects.filter(**journal_data).distinct().order_by('name')
        context |= {
            'semesters': semesters,
            'student_groups': student_groups,
            'disciplines': disciplines,
        }
        return context

    @staticmethod
    def post(request) -> Type[render] | Type[HttpResponse]:
        semester_id = request.POST.get('semester_id', '')
        student_group_id = request.POST.get('student_group_id', '')
        discipline_id = request.POST.get('discipline_id', '')
        selected_journal_data = request.POST.get('selected_journal_data')
        if selected_journal_data:
            selected_journal_json = selected_journal_data.replace('\'', '"')
            selected_journal_data = json.loads(selected_journal_json)
            semester_id = semester_id or selected_journal_data['semester_id']
            student_group_id = student_group_id or selected_journal_data['student_group_id']
            discipline_id = discipline_id or selected_journal_data['discipline_id']

        teacher_id = request.user.teacher.id
        filter_data = {'journal__teacher__id': teacher_id}
        if semester_id:
            filter_data['journal__semester__id'] = semester_id
        if student_group_id:
            filter_data['journal__student_group__id'] = student_group_id
        if discipline_id:
            filter_data['journal__discipline__id'] = discipline_id

        semesters = (Semester.objects.filter(**filter_data).distinct()
                     .order_by('-date_start'))
        student_groups = (StudentGroup.objects.filter(**filter_data).distinct()
                          .order_by('-year_start_studying', 'name'))
        disciplines = (Discipline.objects.filter(**filter_data).distinct()
                       .order_by('name'))

        is_one_semester = semesters.count() == 1
        is_one_student_group = student_groups.count() == 1
        is_one_discipline = disciplines.count() == 1
        if is_one_semester and is_one_student_group and is_one_discipline:
            journal = get_object_or_404(
                Journal,
                discipline__id=disciplines[0].id,
                student_group__id=student_groups[0].id,
                teacher__id=teacher_id,
                semester__id=semesters[0].id
            )
            response = HttpResponse()
            response['HX-Redirect'] = journal.get_absolute_url()
            return response

        # Обновление данных на основе выбора пользователя
        selected_journal_data = {
            'semester_id': semester_id if is_one_semester else '',
            'student_group_id': student_group_id if is_one_student_group else '',
            'discipline_id': discipline_id if is_one_discipline else ''
        }
        context = {
            'semesters': semesters,
            'student_groups': student_groups,
            'disciplines': disciplines,
            'selected_journal_data': selected_journal_data
        }
        return render(request, 'user/inc/teacher/_journal.html', context)
