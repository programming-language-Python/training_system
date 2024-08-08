from typing import Iterable, Type, MutableMapping

from django.forms import inlineformset_factory, ModelForm
from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.testing.abstractions.abstract_views import AbstractFormSetView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm, MaxScoreForm
from apps.testing.models import Testing


class TestingUpdateView(AbstractFormSetView, UpdateView):
    model = Testing
    form_class = TestingForm
    form_set = MaxScoreForm
    template_name = 'testing_update.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context['max_score_form'] = MaxScoreForm(instance=self.object.max_score_set.all()[0])
        return context

    def _get_forms(self) -> Iterable[Type[ModelForm] | Type[inlineformset_factory]]:
        return (
            self.form_class(
                self.request.POST,
                instance=self.get_object()
            ),
            self.form_set(
                self.request.POST,
                instance=self.get_object().max_score_set.all()[0]
            )
        )

    def form_valid(self, form, max_score_form) -> redirect:
        form.save()
        max_score_form.save()
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['pk'])
