from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.views.generic import ListView, DetailView

from testing.models import CompletedTesting
from .forms import UserLoginForm
from .models import User


# Create your views here.
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
            return self.find_completed_testings(query).order_by('-pub_date')
        return CompletedTesting.objects.filter(student=self.request.user)

    def find_completed_testings(self, query):
        q_obj = Q(student=self.request.user)
        print('t')
        if query.isdigit():
            q_obj &= Q(assessment=query)
        else:
            q_obj &= Q(testing__title=query)
        return CompletedTesting.objects.filter(q_obj)


class SearchStudentView(HomeListView):
    def get_queryset(self):
        query = self.request.GET.get('search')
        users = User.objects.annotate(
            full_name=Concat('last_name', Value(' '), 'first_name', Value(' '), 'patronymic')). \
            filter(Q(is_teacher=False) & (Q(full_name__icontains=query) | Q(student_group__title__icontains=query)))
        return users


class TestingCompletedListView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/testing_completed_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['completed_testings'] = CompletedTesting.objects.filter(
                Q(student__in=self.kwargs['pk']) & Q(testing__title=query))
        else:
            context['completed_testings'] = CompletedTesting.objects.filter(student_id=self.kwargs['pk'])
        return context
