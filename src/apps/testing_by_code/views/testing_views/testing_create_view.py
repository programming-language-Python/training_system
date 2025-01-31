from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing_by_code.forms import TestingForm


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm
