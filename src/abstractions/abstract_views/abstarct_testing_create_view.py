from typing import Mapping

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from apps.base_testing.forms import MaxScoreForm
from apps.base_testing.models import MaxScore
from mixins import LoginMixin


class AbstractTestingCreateView(LoginMixin, CreateView):
    template_name = 'testing_create.html'

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= {
            'max_score_header': '<h3>Максимальный балл оценки:</h3>',
            'max_score_form': MaxScoreForm()
        }
        return context

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        max_score_form = MaxScoreForm(self.request.POST)
        if max_score_form.is_valid():
            max_score, is_created = MaxScore.objects.get_or_create(**max_score_form.cleaned_data)
        else:
            return HttpResponse('Форма max_score не валидна')
        form.instance.journal_id = self.kwargs['journal_pk']
        form.instance.max_score = max_score
        response = super().form_valid(form)
        return response
