from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('testing_completed_list/<pk>/', TestingCompletedListView.as_view(), name='testing_completed_list'),
    # path('accounts/profile/', get_user, name='get_user'),
]