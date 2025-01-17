from typing import MutableMapping

from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.abstractions.abstract_views import AbstractFormSetView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm, MaxScoreForm
from apps.testing.models import Testing
from apps.testing.services.testing_service import update_testing
from apps.testing.types import InlineFormSetFactory


class TestingUpdateView(AbstractFormSetView, UpdateView):
    model = Testing
    form_class = TestingForm
    form_set = MaxScoreForm
    template_name = 'testing_update.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context['max_score_form'] = MaxScoreForm(instance=self.object.max_score)
        return context

    def _get_forms(self) -> InlineFormSetFactory:
        return InlineFormSetFactory(
            form=self.form_class(
                self.request.POST,
                instance=self.get_object()
            ),
            form_set=self.form_set(
                self.request.POST,
                instance=self.get_object().max_score
            )
        )

    def form_valid(self, inline_form_set_factory: InlineFormSetFactory) -> redirect:
        update_testing(
            form=inline_form_set_factory.form,
            max_score_form=inline_form_set_factory.form_set
        )
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['pk'])
