from types import NoneType
from typing import Mapping

from django.forms import inlineformset_factory


class AnswerOptionService:
    form_set: inlineformset_factory

    def __init__(self, form_set: inlineformset_factory) -> None:
        self.form_set = form_set

    def get_context_data(self, quantity_answer_options_add: str | NoneType) -> Mapping:
        if quantity_answer_options_add:
            self.set_form_set(
                quantity=self.get_form_set().extra + abs(
                    int(quantity_answer_options_add)
                )
            )
        self.set_attributes_for_form_set()
        return {'answer_option_form_set': self.get_form_set()}

    def get_form_set(self) -> inlineformset_factory:
        return self.form_set

    def add_form_set(self, quantity: int) -> None:
        self.form_set.extra += quantity

    def set_form_set(self, quantity: int) -> None:
        self.form_set.extra = quantity

    def set_attributes_for_form_set(self) -> None:
        for form in self.form_set.forms:
            form.fields['closed_question'].widget.attrs = {
                'data-name': 'closed-question'
            }
            form.fields['DELETE'].widget.attrs = {
                'class': 'uk-checkbox',
                'data-name': 'delete'
            }
