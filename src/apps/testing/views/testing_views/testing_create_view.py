from django.http import HttpResponseRedirect, HttpResponse

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        form.instance.teacher = self.request.user.teacher
        return super(TestingCreateView, self).form_valid(form)
