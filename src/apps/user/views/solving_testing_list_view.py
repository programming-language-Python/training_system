from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.testing.models import SolvingTesting
from apps.testing_by_code.models import SolvingTesting as SolvingTestingByCode
from apps.user.models import Student
from apps.user.services import get_sorted_testings
from apps.user.types import SortingTesting


@method_decorator(login_required, name='dispatch')
class SolvingTestingListView(TemplateView):
    template_name = 'user/student_solving_testing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context |= {
            'student_full_name': Student.objects.get(pk=self.kwargs['student_pk']).user.get_full_name(),
            'solving_testings': self._get_sorted_testings(search),
            'search': search
        }
        return context

    def _get_sorted_testings(self, search: str) -> Iterable[Model]:
        models = [SolvingTesting, SolvingTestingByCode]
        orm_filter = {
            'end_passage__isnull': False,
            'student': self.kwargs['student_pk'],
        }
        if search:
            orm_filter |= {'testing__title__contains': search}
        sorting_field = 'start_passage'
        sorting_testing = SortingTesting(models, orm_filter, sorting_field)
        return get_sorted_testings(sorting_testing)
