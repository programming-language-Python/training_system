from django.urls import reverse_lazy

from abstractions.abstract_views import AbstractTestingDeleteView
from apps.testing.models import Testing


class TestingDeleteView(AbstractTestingDeleteView):
    model = Testing

    def get_success_url(self):
        return reverse_lazy('user:testing_list', kwargs={'journal_pk': self.object.journal_id})
