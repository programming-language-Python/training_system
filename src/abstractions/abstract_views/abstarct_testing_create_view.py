from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


class AbstractTestingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'testing_create.html'
