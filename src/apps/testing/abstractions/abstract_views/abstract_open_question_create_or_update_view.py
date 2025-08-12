from apps.testing.forms.answer_options_forms_set import OpenQuestionAnswerOptionFormSet


class AbstractOpenQuestionCreateOrUpdateView:
    form_set = OpenQuestionAnswerOptionFormSet
    template_name = 'testing/task/task_create_or_update.html'
    table_answer_options_template_name = 'testing/inc/task/answer_options/_table_open_question_answer_options.html'
    answer_options_template_name = 'testing/inc/task/answer_options/_open_question_answer_options.html'
