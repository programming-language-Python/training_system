from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm
from apps.testing.models import Testing
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


# TODO Этот класс дублируется
class TestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing
    template_name = 'testing_list.html'


class TestingDetailView(LoginRequiredMixin, DetailView):
    model = Testing
