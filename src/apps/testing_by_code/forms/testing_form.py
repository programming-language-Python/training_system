from abstractions.abstract_forms import AbstractTestingForm
from apps.testing_by_code.models import Testing


class TestingForm(AbstractTestingForm):

    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        student_groups_value = self.fields.pop('student_groups')
        self.fields['student_groups'] = student_groups_value

    class Meta(AbstractTestingForm.Meta):
        model = Testing
        fields = '__all__'
        exclude = ('teacher', 'date_of_creation', 'date_of_deletion')
