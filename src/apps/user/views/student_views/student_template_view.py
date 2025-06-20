from itertools import chain
from operator import attrgetter
from typing import Mapping

from django.views.generic import TemplateView

from apps.testing.models import SolvingTesting, Testing
from apps.testing_by_code.models import SolvingTesting as SolvingTestingByCode, Testing as TestingByCode
from mixins import LoginMixin


class StudentTemplateView(LoginMixin, TemplateView):
    template_name = 'user/student_detail.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= {
            'testings': self._get_testings(),
            'solving_testings': self._get_solving_testings(),
        }
        return context

    def _get_testings(self) -> list:
        models = [Testing, TestingByCode]
        sorting_field = 'date_of_creation'
        testings = []
        for model in models:
            class_name = model._meta.app_label
            orm_filter = {
                f'{class_name}_solving_testing_set__end_passage__isnull': True,
                'journal__student_group': self.request.user.student.student_group
            }
            testings.append(model.objects.filter(**orm_filter))
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter(sorting_field),
            reverse=True,
        )
        return sorted_testings

    def _get_solving_testings(self) -> list:
        models = [SolvingTesting, SolvingTestingByCode]
        orm_filter = {
            'end_passage__isnull': False,
            'student': self.request.user.student,
        }
        testings = [model.objects.filter(**orm_filter) for model in models]
        sorting_field = 'start_passage'
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter(sorting_field),
            reverse=True,
        )
        return sorted_testings
