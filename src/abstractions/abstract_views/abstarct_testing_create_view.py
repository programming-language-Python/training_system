from django.views.generic import CreateView

from mixins import LoginMixin


class AbstractTestingCreateView(LoginMixin, CreateView):
    template_name = 'testing_create.html'
