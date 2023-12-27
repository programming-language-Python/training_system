from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView

from apps.testing.forms import TestingForm
from apps.testing.models import Testing
from apps.testing_by_code.services.filter_testing import FilterTesting
from apps.testing_by_code.services.find_testing import find_testings


# TODO Этот класс дублируется
class TestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing

    def get_queryset(self) -> QuerySet[Testing]:
        query = self.request.GET.get('search')
        if query:
            return find_testings(
                user=self.request.user,
                title=query
            )
        return self._get_filtered_testing()

    def _get_filtered_testing(self) -> QuerySet[Testing]:
        user = self.request.user
        filter_testing = FilterTesting(user)
        return filter_testing.execute()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context['card_footer_text'] = 'Настроить тестирование'
        else:
            context['card_footer_text'] = 'Пройти тест'
        return context


class TestingCreateView(LoginRequiredMixin, CreateView):
    form_class = TestingForm
    template_name = 'testing_by_code/testing_create.html'

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        is_name_in_completed_testings = CompletedTesting.objects.filter(
            title=form.instance.title
        ).exists()
        if is_name_in_completed_testings:
            return self._add_error_title_exists(form)
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)

    def _add_error_title_exists(self, form) -> HttpResponse:
        form.add_error('title', 'Тестирование с таким Наименование уже существует.')
        context = {
            'form': form
        }
        return render(self.request, 'testing_by_code/testing_create.html', context)
