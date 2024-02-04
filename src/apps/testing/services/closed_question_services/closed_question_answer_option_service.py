from apps.testing.forms.task_forms.сlosed_question_form import ClosedQuestionAnswerOptionFormSet


class ClosedQuestionAnswerOptionService:
    form_set: ClosedQuestionAnswerOptionFormSet

    def __init__(self, form_set: ClosedQuestionAnswerOptionFormSet) -> None:
        self.form_set = form_set

    def get_form_set(self) -> ClosedQuestionAnswerOptionFormSet:
        return self.form_set

    def add_form_set(self, quantity: int) -> None:
        self.form_set.extra += quantity

    def set_form_set(self, quantity: int) -> None:
        self.form_set.extra = quantity

    def set_attributes_for_form_set(self) -> None:
        for form in self.form_set.forms:
            form.fields['closed_question'].widget.attrs = {
                'data-name': 'closed-question'
            }
            form.fields['DELETE'].widget.attrs = {
                'class': 'uk-checkbox',
                'data-name': 'delete'
            }
