import json
from typing import Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.user.models import Semester, StudentGroup, Discipline, Journal, Student


class TestingResultJournalView(LoginRequiredMixin, View):
    @staticmethod
    def post(request) -> Type[render] | Type[HttpResponse]:
        semester_id = request.POST.get('semester_id', '')
        student_group_id = request.POST.get('student_group_id', '')
        discipline_id = request.POST.get('discipline_id', '')
        student_id = request.POST.get('student_id', '')

        selected_journal_data = request.POST.get('selected_journal_2_data')
        if selected_journal_data:
            selected_journal_json = selected_journal_data.replace('\'', '"')
            selected_journal_data = json.loads(selected_journal_json)
            semester_id = semester_id or selected_journal_data['semester_id']
            student_group_id = student_group_id or selected_journal_data['student_group_id']
            discipline_id = discipline_id or selected_journal_data['discipline_id']
            student_id = student_id or selected_journal_data['student_id']

        teacher_id = request.user.teacher.id
        filter_data = {'teacher': teacher_id}
        if semester_id:
            filter_data['semester'] = semester_id
        if student_group_id:
            filter_data['student_group'] = student_group_id
        if discipline_id:
            filter_data['discipline'] = discipline_id
        if student_id:
            filter_data['student_group__student'] = student_id

        journals = Journal.objects.filter(**filter_data).distinct()
        is_one_journal = journals.count() == 1
        if is_one_journal and student_id:
            response = HttpResponse()
            kwargs = {
                'student_pk': student_id,
                'journal_pk': journals.first().pk
            }
            response['HX-Redirect'] = reverse(f'user:solving_testing_list', kwargs=kwargs)
            return response

        # Обновление данных на основе выбора пользователя
        selected_journal_data = {
            'semester_id': semester_id,
            'student_group_id': student_group_id,
            'discipline_id': discipline_id,
            'student_id': student_id
        }
        semesters = Semester.objects.filter(pk__in=journals.values_list('semester', flat=True))
        student_groups = StudentGroup.objects.filter(pk__in=journals.values_list('student_group', flat=True))
        disciplines = Discipline.objects.filter(pk__in=journals.values_list('discipline', flat=True))
        if student_id:
            student_filter = {'pk': student_id}
        else:
            student_filter = {'student_group__in': student_groups}
        students = Student.objects.filter(**student_filter)
        journal_data = {
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
            'Студенты': {
                'model_name': 'student',
                'objects': students
            }
        }
        context = {
            'selected_journal_data': selected_journal_data,
            'journal_data': journal_data,
            'journal_url': 'user:testing_result_journal',
            'target': request.GET.get('target', 'journal_2')
        }
        return render(request, 'user/inc/journal/_journal.html', context)
