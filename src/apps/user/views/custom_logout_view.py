from django.contrib.auth.views import LogoutView

from config import settings


class CustomLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
