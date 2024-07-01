from abstractions.abstract_forms import AbstractTestingForm
from apps.testing_by_code.models import Testing


class TestingForm(AbstractTestingForm):

    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        student_groups_value = self.fields.pop('student_groups')
        self.fields['student_groups'] = student_groups_value

    class Meta:
        model = Testing
        fields = (
            'title',
            'student_groups',
            'is_published',
            'is_review_of_result_by_student'
        )
