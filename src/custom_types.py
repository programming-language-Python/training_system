from dataclasses import dataclass, fields
from typing import Type, Iterable

from django.forms import ModelForm, inlineformset_factory


@dataclass
class InlineFormSetFactory:
    form: ModelForm
    form_set: ModelForm | Type[inlineformset_factory]
    additional_form: ModelForm | None = None

    @property
    def forms(self) -> Iterable:
        forms = []
        for field in fields(self):
            field_value = getattr(self, field.name)
            if field_value:
                forms.append(field_value)
        return forms
