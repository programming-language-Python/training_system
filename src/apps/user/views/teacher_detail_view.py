from typing import Mapping

from django.db.models import Value, Q
from django.db.models.functions import Concat
from django.views.generic import DetailView

from apps.user.models import User, Student
from mixins import LoginMixin


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
