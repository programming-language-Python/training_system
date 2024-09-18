from django.urls import reverse_lazy

from abstractions.abstract_views import AbstractTestingDeleteView
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class TestingDeleteView(AbstractTestingDeleteView):
    model = Testing
    success_url = reverse_lazy(APP_NAME + ':testing_list')
