from abstractions.abstract_views import AbstractTestingUpdateView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm
from apps.testing.models import Testing


class TestingUpdateView(AbstractTestingUpdateView):
    APP_NAME = APP_NAME
    model = Testing
    form_class = TestingForm
