from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.testing.models import Testing
from apps.testing_by_code.models import Testing as TestingByCode
from apps.user.services import get_sorted_testings
from apps.user.types import SortingTesting


@method_decorator(login_required, name='dispatch')
class TestingListView(TemplateView):
    template_name = 'testing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_teacher():
            text = 'Настроить'
        else:
            text = 'Пройти тест'
        search = self.request.GET.get('search', '')
        context |= {
            'text': text,
            'testing_list': self._get_sorted_testings(search),
            'search': search
        }
        return context

    def _get_sorted_testings(self, search: str) -> Iterable[Model]:
        models = [Testing, TestingByCode]
        orm_filter = {'journal': self.kwargs['journal_pk']}
        if search:
            orm_filter |= {'title__contains': search}
        sorting_field = 'date_of_creation'
        sorting_testing = SortingTesting(models, orm_filter, sorting_field)
        return get_sorted_testings(sorting_testing)
