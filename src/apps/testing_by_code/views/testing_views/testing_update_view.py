from abstractions.abstract_views import AbstractTestingUpdateView
from apps.testing_by_code.constants import APP_NAME
from apps.testing_by_code.forms import TestingForm
from apps.testing_by_code.models import Testing


class TestingUpdateView(AbstractTestingUpdateView):
    APP_NAME = APP_NAME
    model = Testing
    form_class = TestingForm
