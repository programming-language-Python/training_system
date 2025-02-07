import json
from typing import Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.user.models import Journal, Semester, Discipline, Teacher


class StudentJournalView(LoginRequiredMixin, View):
    @staticmethod
    def post(request) -> Type[render] | Type[HttpResponse]:
        semester_id = request.POST.get('semester_id', '')
        discipline_id = request.POST.get('discipline_id', '')
        teacher_id = request.POST.get('teacher_id', '')

        selected_journal_data = request.POST.get('selected_journal_data')
        if selected_journal_data:
            selected_journal_json = selected_journal_data.replace('\'', '"')
            selected_journal_data = json.loads(selected_journal_json)
            semester_id = semester_id or selected_journal_data['semester_id']
            discipline_id = discipline_id or selected_journal_data['discipline_id']
            teacher_id = teacher_id or selected_journal_data['teacher_id']

        filter_data = {'student_group': request.user.student.student_group}
        if semester_id:
            filter_data['semester'] = semester_id
        if discipline_id:
            filter_data['discipline'] = discipline_id
        if teacher_id:
            filter_data['teacher'] = teacher_id

        journals = Journal.objects.filter(**filter_data).distinct()
        is_one_journal = journals.count() == 1
        if is_one_journal:
            response = HttpResponse()
            kwargs = {
                'student_pk': request.user.student.id,
                'journal_pk': journals.first().pk
            }
            response['HX-Redirect'] = reverse(f'user:solving_testing_list', kwargs=kwargs)
            return response

        # Обновление данных на основе выбора пользователя
        selected_journal_data = {
            'semester_id': semester_id,
            'discipline_id': discipline_id,
            'teacher_id': teacher_id,
        }
        semesters = Semester.objects.filter(pk__in=journals.values_list('semester', flat=True))
        disciplines = Discipline.objects.filter(pk__in=journals.values_list('discipline', flat=True))
        teachers = Teacher.objects.filter(pk__in=journals.values_list('teacher', flat=True))
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
        context = {
            'selected_journal_data': selected_journal_data,
            'journal_data': journal_data,
            'journal_url': 'user:student_journal',
            'target': request.GET.get('target', 'journal')
        }
        return render(request, 'user/inc/journal/_journal.html', context)
