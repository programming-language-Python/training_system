from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from apps.user.forms import UserLoginForm


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self) -> reverse_lazy:
        if self.request.user.is_authenticated:
            return self.get_success_url()
        return super().get_redirect_url()

    def get_success_url(self) -> reverse_lazy:
        if self.request.user.is_teacher():
            return reverse_lazy(f'user:teacher_detail')
        return reverse_lazy(f'user:student_detail')
