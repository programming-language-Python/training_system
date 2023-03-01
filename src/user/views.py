from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView

from testing.models import CompletedTesting
from .forms import UserLoginForm
from .models import User


# Create your views here.
class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'


class HomeListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    template_name = 'user/user_detail.html'
    context_object_name = 'home_list'

    def get_queryset(self):
        if self.request.user.is_teacher:
            return User.objects.filter(is_teacher=False)
        return CompletedTesting.objects.filter(student=self.request.user)


class TestingCompletedListView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/testing_completed_list.html'
