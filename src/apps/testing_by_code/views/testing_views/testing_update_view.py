from django.views.generic import UpdateView

from apps.testing_by_code.forms import TestingForm
from apps.testing_by_code.models import Testing
from mixins import LoginMixin


class TestingUpdateView(LoginMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name = 'testing_update.html'
