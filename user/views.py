from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .models import User


# Create your views here.

def redirect_get_user_or_login(request):
    if request.user.is_authenticated:
        return redirect('user:get_user')
    return redirect('user:login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'


def get_user(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'user/user.html', {'user': user})
