from typing import Iterable

from django.db import models


def get_field_values(model: models.Model, excluded_fields: Iterable[str]) -> Iterable[str]:
    field_values = []
    for field in model.__class__._meta.fields:
        if field.name not in excluded_fields:
            if field.value_from_object(model):
                if isinstance(field.value_from_object(model), bool):
                    field_values.append(f'{field.verbose_name}: да')
                else:
                    field_values.append(f'{field.verbose_name}: {field.value_from_object(model)}')
            else:
                field_values.append(f'{field.verbose_name}: нет')
    return field_values
