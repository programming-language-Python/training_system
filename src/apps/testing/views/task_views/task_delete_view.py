from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.testing.abstractions.abstract_views import AbstractTaskView
from mixins import LoginMixin


class TaskDeleteView(AbstractTaskView, LoginMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(f'testing:teacher_testing_detail', kwargs={'pk': self.request.GET['testing_pk']})
