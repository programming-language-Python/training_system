from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm
from apps.testing.models import Testing
from apps.testing.models.completed_testing import CompletedTesting
from mixins import URLMixin, ContextMixin


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
class TestingListView(ContextMixin, LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing
    template_name = 'testing_list.html'
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_list_data(is_teacher=self.request.user.is_teacher)
        return context


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context |= self.get_testing_detail_url_button_data()
        return context


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name = 'testing_update.html'


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy(APP_NAME + ':testing_list')
    template_name = 'testing_confirm_delete.html'


def add_task_form():
    pass
