from apps.testing.forms.answer_options_forms_set import AnswerOptionFormSet


class AbstractTaskWithChoiceCreateOrUpdateView:
    form_set = AnswerOptionFormSet
    template_name = 'testing/task/task_with_choice_create_or_update.html'
    table_answer_options_template_name = 'testing/inc/task/answer_options/_table_answer_options_with_choice.html'
    answer_options_template_name = 'testing/inc/task/answer_options/_answer_options_with_choice.html'
