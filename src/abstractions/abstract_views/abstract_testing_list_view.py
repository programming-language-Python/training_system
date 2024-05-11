from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView


class AbstractTestingListView(LoginRequiredMixin, ListView):
    login_url = 'user:login'

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('search')
        if query:
            return find_testings(
                user=self.request.user,
                title=query
            )
        return self._get_filtered_testing()

    def _get_filtered_testing(self) -> QuerySet:
        user = self.request.user
        filter_testing = FilterTesting(user)
        return filter_testing.execute()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher()
        if is_teacher_:
            context['card_footer_text'] = 'Настроить тестирование'
        else:
            context['card_footer_text'] = 'Пройти тест'
        return context
