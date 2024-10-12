from apps.testing.abstractions.abstract_views import AbstractTaskUpdateView
from apps.testing.forms.task_forms.sequencing_form import SequencingForm, SequencingAnswerOptionFormSet
from apps.testing.models.tasks import Sequencing


class SequencingUpdateView(AbstractTaskUpdateView):
    model = Sequencing
    form_class = SequencingForm
    form_set = SequencingAnswerOptionFormSet
    template_name = 'testing/task/task_with_answer_option_with_checkbox.html'
    answer_options_template_name = 'testing/inc/task/table/_table_answer_option_with_checkbox.html'
