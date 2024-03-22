from django import forms

from apps.testing.models import CompletedOpenQuestion


class OpenQuestionAnswerForm(forms.ModelForm):
    def clean(self):
        pass

    class Meta:
        model = CompletedOpenQuestion
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
        exclude = ['type', 'completed_testing', ]
