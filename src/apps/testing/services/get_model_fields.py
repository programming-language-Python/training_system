from typing import Iterable, Type

from django.db import models


def get_model_fields(model: models.Model | Type[models.Model], excluded_fields: Iterable[str]) -> Iterable:
    fields = []
    for field in model._meta.fields:
        if field.name not in excluded_fields:
            fields.append(field)
    return fields
