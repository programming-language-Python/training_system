from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from apps.user.constants import APP_NAME
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
        kwargs = {'pk': self.request.user.pk}
        if self.request.user.is_teacher():
            return reverse_lazy(f'{APP_NAME}:teacher_detail', kwargs=kwargs)
        return reverse_lazy(f'{APP_NAME}:student_detail', kwargs=kwargs)
