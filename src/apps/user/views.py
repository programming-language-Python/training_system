from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.views.generic import ListView, DetailView

from config import settings
from apps.testing_by_code.models import SolvingTesting
from apps.testing_by_code.services.find_testing import find_solved_testings
from .forms import UserLoginForm
from .models import Student, User


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'


class HomeListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    template_name = 'user/user_detail.html'
    context_object_name = 'home_list'

    def get_queryset(self):
        if self.request.user.is_teacher():
            return Student.objects.all()
        query = self.request.GET.get('search')
        if query:
            return find_solved_testings(
                student=self.request.user.student,
                query=query
            )
        return SolvingTesting.objects.filter(student=self.request.user.student)


class SearchStudentView(HomeListView):
    def get_queryset(self):
        query = self.request.GET.get('search')
        students = Student.objects.annotate(
            full_name=Concat(
                'user__last_name',
                Value(' '),
                'user__first_name',
                Value(' '),
                'user__patronymic'
            )
        ).filter(
            Q(full_name__icontains=query)
            | Q(student_group__name__icontains=query)
        )
        return students


class TestingCompletedListView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/testing_completed_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['solving_testings'] = SolvingTesting.objects.filter(
                Q(student__in=self.kwargs['pk']) & Q(title=query)
            )
        else:
            context['solving_testings'] = SolvingTesting.objects.filter(student_id=self.kwargs['pk'])
        return context


class CustomLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
