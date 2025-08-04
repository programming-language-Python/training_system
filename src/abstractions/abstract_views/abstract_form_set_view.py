from typing import Type, MutableMapping

from django.forms import inlineformset_factory, ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from custom_types import InlineFormSetFactory


class AbstractFormSetView:
    form_set: Type[ModelForm] | Type[inlineformset_factory]
    template_name: str
    table_answer_options_template_name: str
    answer_options_template_name: str

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Для UpdateView
            self.object = self.get_object()
        else:
            # Для CreateView
            self.object = None
        if request.GET.get('quantity-answer-options-add'):
            context = self.get_context_data()
            html = render_to_string(self.answer_options_template_name, context, request=request)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> redirect:
        forms = self._get_forms()
        if all(form.is_valid() for form in forms.forms):
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

    def _get_forms(self) -> InlineFormSetFactory:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_valid(self, inline_form_set_factory: InlineFormSetFactory) -> redirect:
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')

    def form_invalid(self, inline_form_set_factory: InlineFormSetFactory) -> redirect:
        self.object = None
        form = inline_form_set_factory.form
        form_set = inline_form_set_factory.form_set
        forms_context = {
            'form': form,
            'form_set': form_set,
            'form_errors': form.errors,
            'form_set_errors': form_set.errors,
        }
        additional_form = inline_form_set_factory.additional_form
        if additional_form:
            forms_context |= {
                'additional_form': additional_form,
                'additional_form_errors': additional_form.errors
            }
        return self.render_to_response(self.get_context_data(**forms_context))
