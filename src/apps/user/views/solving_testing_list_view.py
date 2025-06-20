from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.testing.models import SolvingTesting
from apps.testing_by_code.models import SolvingTesting as SolvingTestingByCode
from apps.user.models import Student


@method_decorator(login_required, name='dispatch')
class SolvingTestingListView(TemplateView):
    template_name = 'user/student_solving_testing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'student_full_name': Student.objects.get(pk=self.kwargs['student_pk']).user.get_full_name(),
            'solving_testings': self._get_testings()
        }
        return context

    def _get_testings(self) -> list:
        models = [SolvingTesting, SolvingTestingByCode]
        orm_filter = {
            'end_passage__isnull': False,
            'student': self.kwargs['student_pk'],
        }
        testings = [model.objects.filter(**orm_filter) for model in models]
        sorting_field = 'start_passage'
        sorted_testings = sorted(
            chain(*testings),
            key=attrgetter(sorting_field),
            reverse=True,
        )
        return sorted_testings
