from typing import Mapping

from apps.testing.models import Testing


class ClosedQuestionService:
    testing_pk: int

    def __init__(self, testing_pk: int) -> None:
        self.testing_pk = testing_pk

    def set_initial_values_form_fields(self, fields: Mapping) -> Mapping:
        fields['serial_number'].initial = self.get_quantity() + 1
        fields['testing'].initial = self.testing_pk
        return fields

    def get_quantity(self) -> int:
        return Testing.objects.get(pk=self.testing_pk).closed_question_set.count()
