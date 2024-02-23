from django import forms

from apps.testing.models.tasks.open_question import OpenQuestionAnswerOption


class OpenQuestionCheckAnswerForm(forms.Form):
    your_answer = forms.CharField()

    # def clean(self):
    #     cleaned_data = super(OpenQuestionCheckAnswerForm, self).clean()
    #     response = cleaned_data.get("your_answer")
    #     # try:
    #     p = OpenQuestionAnswerOption.objects.filter(correct_answer__iexact=response)
    #     print()
    #     # if (
    #     #         your_answer == p.answer and your_question == p.question_relation.question_text):  # user inputs should be matched with the Answer of that particular Question
    #     # # Code To Run for Correct Answer Goes Here
    #     # else:
    #     #     # The Answer is Wrong or Does not Match the Particular Question
    #     #     raise forms.ValidationError("Wrong Answer.")
    #     # except Answer.DoesNotExist:
    #     #     raise forms.ValidationError("Wrong Answer.")
