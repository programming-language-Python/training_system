from typing import Mapping

from django.http import HttpResponseRedirect, HttpResponse

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm, MaxScoreForm
from apps.testing.models import MaxScore


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

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
        form.instance.teacher = self.request.user.teacher
        form.instance.max_score = max_score
        response = super(TestingCreateView, self).form_valid(form)
        return response
