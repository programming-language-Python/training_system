from typing import Iterable

from django.db.models import Q, QuerySet
from django.forms import ModelMultipleChoiceField, ChoiceField

from apps.testing_by_code.forms import SettingForm
from apps.testing_by_code.models import Setting
from apps.testing_by_code.types import Cycle

PRIORITY_FIELDS = (
    'is_OOP',
    'is_strings'
)


class FilterSetting:
    setting_filter: QuerySet[Setting]
    setting_form: SettingForm
    q_obj: Q

    def __init__(self, setting_form: SettingForm) -> None:
        self.setting_filter = Setting.objects
        self.setting_form = setting_form
        self.q_obj = Q()

    def execute(self) -> QuerySet[Setting]:
        for field_name, field in self.setting_form.fields.items():
            self._filter_field(field_name, field)
        return self.setting_filter.filter(self.q_obj)

    def _filter_field(self, field_name: str, field: ChoiceField) -> None:
        if isinstance(field, ModelMultipleChoiceField):
            self._filter_many_to_many_fields(field_name, field)
        else:
            q_filter = {
                f'{field_name}': self.setting_form.cleaned_data[field_name]
            }
            self.q_obj &= Q(**q_filter)

    def _filter_many_to_many_fields(self, field_name: str, field: ChoiceField) -> None:
        excluded_choices = [choice[1] for choice in field.choices]
        for item in self.setting_form.cleaned_data[field_name]:
            item_filter = {f'{field_name}__title': item.title}
            self.setting_filter = self.setting_filter.filter(**item_filter)
            excluded_choices.remove(f'{item}')
        if excluded_choices:
            self._filter_excluded_many_to_many_fields(
                field_name,
                excluded_choices
            )

    def _filter_excluded_many_to_many_fields(self, field_name: str,
                                             excluded_choices: Iterable[Cycle]) -> None:
        for excluded_choice in excluded_choices:
            excluded_choice_filter = {f'{field_name}__title': excluded_choice}
            self.setting_filter = self.setting_filter.exclude(
                **excluded_choice_filter
            )
