from abstractions.abstract_forms import AbstractTestingForm
from apps.testing_by_code.models import Testing


class TestingForm(AbstractTestingForm):
    class Meta(AbstractTestingForm.Meta):
        model = Testing
        exclude = ('date_of_deletion', 'journal', 'total_weight', 'max_score')
