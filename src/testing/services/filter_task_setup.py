from django.db.models import Q, Manager
from django.forms import ModelMultipleChoiceField, Form

from testing.models import TaskSetup


class FilterSetup:
    setup_filter: Manager[TaskSetup]
    setup_form: Form
    q_obj: Q

    def __init__(self, setup: Manager[TaskSetup], setup_form: Form) -> None:
        self.setup_filter = setup
        self.setup_form = setup_form
        self.q_obj = Q()

    def execute(self) -> Manager:
        for field_name, field in self.setup_form.fields.items():
            self._filter_field(field_name, field)
        return self.setup_filter.filter(self.q_obj)

    def _filter_field(self, field_name, field) -> None:
        if isinstance(field, ModelMultipleChoiceField):
            self._filter_many_to_many_fields(field_name, field)
        else:
            q_filter = {
                f'{field_name}': self.setup_form.cleaned_data[field_name]
            }
            self.q_obj &= Q(**q_filter)

    def _filter_many_to_many_fields(self, field_name, field) -> None:
        excluded_choices = [choice[1] for choice in field.choices]
        for item in self.setup_form.cleaned_data[field_name]:
            item_filter = {f'{field_name}__title': item.title}
            self.setup_filter = self.setup_filter.filter(**item_filter)
            excluded_choices.remove(f'{item}')
        if excluded_choices:
            self._filter_excluded_many_to_many_fields(
                field_name,
                excluded_choices
            )

    def _filter_excluded_many_to_many_fields(self, field_name,
                                             excluded_choices) -> None:
        for excluded_choice in excluded_choices:
            excluded_choice_filter = {f'{field_name}__title': excluded_choice}
            self.setup_filter = self.setup_filter.exclude(
                **excluded_choice_filter
            )
