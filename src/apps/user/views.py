from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.views.generic import ListView, DetailView

from config import settings
from apps.testing_by_code.models import CompletedTesting
from apps.testing_by_code.services.find_testing import find_completed_testings
from .forms import UserLoginForm
from .models import User


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
        query = self.request.GET.get('search')
        if query:
            return find_completed_testings(
                user=self.request.user,
                query=query
            )
        return CompletedTesting.objects.filter(student=self.request.user)


class SearchStudentView(HomeListView):
    def get_queryset(self):
        query = self.request.GET.get('search')
        users = User.objects.annotate(
            full_name=Concat(
                'last_name',
                Value(' '),
                'first_name',
                Value(' '),
                'patronymic'
            )
        ). \
            filter(
            Q(is_teacher=False)
            & (
                    Q(full_name__icontains=query)
                    | Q(student_group__title__icontains=query)
            )
        )
        return users


class TestingCompletedListView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/testing_completed_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['completed_testings'] = CompletedTesting.objects.filter(
                Q(student__in=self.kwargs['pk']) & Q(title=query)
            )
        else:
            context['completed_testings'] = CompletedTesting.objects.filter(student_id=self.kwargs['pk'])
        return context


class CustomLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
