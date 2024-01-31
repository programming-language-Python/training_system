from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy(APP_NAME + ':testing_list')
    template_name = 'testing_confirm_delete.html'
