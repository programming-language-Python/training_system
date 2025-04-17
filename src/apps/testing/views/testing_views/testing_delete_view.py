from django.urls import reverse_lazy

from abstractions.abstract_views import AbstractTestingDeleteView
from apps.testing.models import Testing


class TestingDeleteView(AbstractTestingDeleteView):
    model = Testing
    success_url = reverse_lazy('user:testing_list')
