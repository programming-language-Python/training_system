from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm
