from django.contrib.auth.mixins import LoginRequiredMixin


class LoginMixin(LoginRequiredMixin):
    login_url = 'user:home'
