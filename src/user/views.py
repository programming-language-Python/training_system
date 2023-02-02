from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from testing.models import CompletedTesting
from .forms import UserLoginForm


# Create your views here.
class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'


class CompletedTestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = CompletedTesting
    template_name = 'user/user_detail.html'

    def get_queryset(self):
        return CompletedTesting.objects.filter(student=self.request.user)
