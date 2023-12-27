from abstractions.abstract_forms.AbstractTestingForm import AbstractTestingForm
from apps.testing.models import Testing


class TestingForm(AbstractTestingForm):
    class Meta:
        model = Testing
        fields = (
            'title',
            'student_groups',
            'is_published',
            'is_review_of_result_by_student'
        )
