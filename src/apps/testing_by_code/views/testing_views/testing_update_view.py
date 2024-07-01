from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from apps.testing_by_code.forms import TestingForm
from apps.testing_by_code.models import Testing


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name = 'testing_update.html'
