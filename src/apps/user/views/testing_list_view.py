from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.testing.models import Testing
from apps.testing_by_code.models import Testing as TestingByCode


@method_decorator(login_required, name='dispatch')
class TestingListView(TemplateView):
    template_name = 'testing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_teacher():
            text = 'Настроить тестирование'
        else:
            text = 'Пройти тест'
        context |= {
            'text': text,
            'testing_list': self._get_testings(journal_pk=kwargs['journal_pk'])
        }
        return context

    @staticmethod
    def _get_testings(journal_pk: int | str):
        models = [Testing, TestingByCode]
        orm_filter = {'journal': journal_pk}
        testings = [model.objects.filter(**orm_filter) for model in models]
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter('date_of_creation'),
            reverse=True,
        )
        return sorted_testings
