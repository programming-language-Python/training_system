from typing import Iterable, Type

from django.forms import inlineformset_factory, ModelForm
from django.shortcuts import redirect
from django.views.generic.base import TemplateResponseMixin

from mixins import LoginMixin


class AbstractFormSetView(LoginMixin):
    form_set: Type[ModelForm] | Type[inlineformset_factory]
    template_name: str

    def post(self, request, *args, **kwargs) -> redirect:
        form, form_set = self._get_forms()
        if form.is_valid() and form_set.is_valid():
            return self.form_valid(form, form_set)
        else:
            return self.form_invalid(form, form_set)

    def _get_forms(self) -> Iterable[Type[ModelForm] | Type[inlineformset_factory]]:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_valid(self, form, form_set) -> redirect:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_invalid(self, form, form_set) -> redirect:
        self.object = None
        return TemplateResponseMixin.render_to_response(
            self.get_context_data(
                form=form,
                form_set=form_set,
                # form_set_errors=form_set.errors
            )
        )
