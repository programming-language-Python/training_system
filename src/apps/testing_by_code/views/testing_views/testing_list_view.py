from django.db.models import QuerySet
from django.views.generic import ListView

from apps.testing_by_code.models import Testing
from apps.testing_by_code.services.filter_testing import FilterTesting
from apps.testing_by_code.services.find_testing import find_testings
from mixins import ContextMixin, LoginMixin
from apps.testing_by_code.constants import APP_NAME


class TestingListView(LoginMixin, ContextMixin, ListView):
    model = Testing
    template_name = 'testing_list.html'
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_list_data(is_teacher=self.request.user.is_teacher())
        return context

    def get_queryset(self) -> QuerySet[Testing]:
        query = self.request.GET.get('search')
        if query:
            return find_testings(
                user=self.request.user,
                title=query
            )
        return self._get_filtered_testing()

    def _get_filtered_testing(self) -> QuerySet[Testing]:
        user = self.request.user
        filter_testing = FilterTesting(user)
        return filter_testing.execute()
