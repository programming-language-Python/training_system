from itertools import chain
from operator import attrgetter
from typing import Mapping

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView

from apps.testing.models import SolvingTesting, Testing
from apps.testing_by_code.models import SolvingTesting as SolvingTestingByCode, Testing as TestingByCode
from mixins import LoginMixin


class StudentTemplateView(LoginMixin, TemplateView):
    template_name = 'user/student_detail.html'
    paginate_by = 10

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)

        testings = self._get_testings()
        testings_paginator = Paginator(testings, self.paginate_by)
        testings_page_number = self.request.GET.get('page_testings', 1)
        testings_page = self._get_page(
            paginator=testings_paginator,
            number=testings_page_number
        )

        solving_testings = self._get_solving_testings()
        solving_paginator = Paginator(solving_testings, self.paginate_by)
        solving_page_number = self.request.GET.get('page_solving', 1)
        solving_page = self._get_page(
            paginator=solving_paginator,
            number=solving_page_number
        )

        context |= {
            'testings': testings_page,
            'solving_testings': solving_page,
            'testings_paginator': testings_paginator,
            'solving_paginator': solving_paginator,
        }
        return context

    def _get_testings(self) -> list:
        models = [Testing, TestingByCode]
        sorting_field = 'date_of_creation'
        testings = []
        for model in models:
            class_name = model._meta.app_label
            orm_filter = {
                f'{class_name}_solving_testing_set__assessment__isnull': True,
                'journal__student_group': self.request.user.student.student_group
            }
            testings.append(
                model.objects.filter(**orm_filter)
                .select_related('journal')
                .select_related('journal__semester')
                .select_related('journal__discipline')
                .select_related('journal__teacher')
            )
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter(sorting_field),
            reverse=True,
        )
        return sorted_testings

    def _get_solving_testings(self) -> list:
        models = [SolvingTesting, SolvingTestingByCode]
        orm_filter = {
            'assessment__isnull': False,
            'student': self.request.user.student,
        }
        testings = [model.objects.filter(**orm_filter)
                    .select_related('testing')
                    .select_related('testing__journal')
                    .select_related('testing__journal__semester')
                    .select_related('testing__journal__discipline')
                    .select_related('testing__journal__teacher')
                    for model in models]
        sorting_field = 'start_passage'
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter(sorting_field),
            reverse=True,
        )
        return sorted_testings

    @staticmethod
    def _get_page(paginator: Paginator, number: int) -> Paginator:
        try:
            page = paginator.page(number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
