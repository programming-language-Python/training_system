from django import forms

from apps.testing.models.solving_tasks.solving_open_question import SolvingOpenQuestion


class OpenQuestionAnswerForm(forms.ModelForm):
    def clean(self):
        pass

    class Meta:
        model = SolvingOpenQuestion
        widgets = {
            'serial_number': forms.TextInput(
                attrs={
                    'class': 'serial-number',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'serial-number',
                }
            ),
        }
        exclude = ['type', 'solving_testing', ]
