from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import UserLoginForm


# Create your views here.
class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'


@login_required
def get_user(request):
    return render(request, 'user/user_detail.html')
