from typing import Mapping

from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import DetailView

from config import settings
from mixins import LoginMixin
from .constants import APP_NAME
from .forms import UserLoginForm
from .mixins import StudentSolvingTestingListMixin
from .models import Student, User
from ..testing.models import SolvingTesting
from ..testing_by_code.models import SolvingTesting as SolvingTestingByCode


class StudentSolvingTestingListView(StudentSolvingTestingListMixin):
    model = SolvingTesting


class StudentSolvingTestingByCodeListView(StudentSolvingTestingListMixin):
    model = SolvingTestingByCode


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


class TeacherDetailView(LoginMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['students'] = Student.objects.annotate(
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
        else:
            context['students'] = Student.objects.all()
        return context


class StudentDetailView(LoginMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'


class CustomLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
