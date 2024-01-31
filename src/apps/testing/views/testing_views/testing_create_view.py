from django.http import HttpResponse, HttpResponseRedirect

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm
from apps.testing.models.completed_testing import CompletedTesting


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        is_title_in_completed_testings = CompletedTesting.objects.filter(
            title=form.instance.title
        ).exists()
        if is_title_in_completed_testings:
            return self._add_error_title_exists(form)
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)
