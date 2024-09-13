from typing import Mapping

from django.http import HttpResponseRedirect, HttpResponse

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.forms import TestingForm, MaxScoreForm


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
        form.instance.teacher = self.request.user.teacher
        response = super(TestingCreateView, self).form_valid(form)
        max_score_form = MaxScoreForm(self.request.POST)
        max_score_form.save()
        max_score_form.instance.testing.add(form.instance.pk)
        return response
