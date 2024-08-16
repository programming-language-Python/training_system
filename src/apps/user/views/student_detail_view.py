from django.views.generic import DetailView

from apps.user.models import User
from mixins import LoginMixin


class StudentDetailView(LoginMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'
