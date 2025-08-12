from typing import MutableMapping

from apps.testing.forms.answer_options_forms_set import AnswerOptionFormSet


class AbstractSequencingCreateOrUpdateView:
    form_set = AnswerOptionFormSet
    template_name = 'testing/task/task_with_choice_create_or_update.html'
    table_answer_options_template_name = 'testing/inc/task/answer_options/_table_sequencing_answer_options.html'
    answer_options_template_name = 'testing/inc/task/answer_options/_sequencing_answer_options.html'

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        forms = context['answer_option_form_set'].forms
        forms_with_correct_options_answers = []
        forms_with_incorrect_options_answers = []
        for form in forms:
            if form['is_correct'].value():
                forms_with_correct_options_answers.append(form)
            else:
                forms_with_incorrect_options_answers.append(form)
        context |= {
            'forms_with_correct_options_answers': forms_with_correct_options_answers,
            'forms_with_incorrect_options_answers': forms_with_incorrect_options_answers
        }
        return context
