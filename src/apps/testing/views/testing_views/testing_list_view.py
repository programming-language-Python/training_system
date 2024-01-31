from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from mixins import ContextMixin


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
