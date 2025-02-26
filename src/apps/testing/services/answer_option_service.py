from types import NoneType
from typing import Mapping, Type

from django.forms import inlineformset_factory


class AnswerOptionService:
    form_set: Type[inlineformset_factory]

    def __init__(self, form_set: Type[inlineformset_factory]) -> None:
        self.form_set = form_set

    def get_context_data(self, quantity_answer_options_add: str | NoneType) -> Mapping:
        if quantity_answer_options_add:
            self._set_form_set(
                quantity=self.form_set.extra + abs(
                    int(quantity_answer_options_add)
                )
            )
        self._set_attributes_for_form_set()
        return {'answer_option_form_set': self.form_set}

    def _set_form_set(self, quantity: int) -> None:
        self.form_set.extra = quantity

    def _set_attributes_for_form_set(self) -> None:
        task_name = self.form_set.fk.attname.replace('_id', '')
        for form in self.form_set.forms:
            form.fields[task_name].widget.attrs = {
                'data-name': task_name.replace('_', '-')
            }
            form.fields['DELETE'].widget.attrs = {
                'class': 'uk-checkbox',
                'data-name': 'delete'
            }
