from django.http import HttpResponse, HttpResponseRedirect

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing_by_code.forms import TestingForm


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        form.instance.teacher = self.request.user.teacher
        return super(TestingCreateView, self).form_valid(form)
