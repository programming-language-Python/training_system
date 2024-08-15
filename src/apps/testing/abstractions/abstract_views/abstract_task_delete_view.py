from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.testing.constants import APP_NAME
from mixins import LoginMixin


class AbstractTaskDeleteView(LoginMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(f'{APP_NAME}:testing_detail', kwargs={'pk': self.request.GET['testing_pk']})
