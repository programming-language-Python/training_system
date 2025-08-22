from django import forms

from apps.testing.models import SolvingTask


class SolvingTaskForm(forms.ModelForm):
    answer = forms.CharField(
        label='Ответ',
        required=False,
        widget=forms.TextInput()
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.score = instance.task.service.get_score(self.cleaned_data['answer'])
        instance.save()
        return instance

    class Meta:
        model = SolvingTask
        fields = ('time_left', 'answer',)
        widgets = {
            'time_left': forms.TextInput(attrs={
                'class': 'uk-margin-small uk-input uk-width-small',
                'type': 'text',
                'tabindex': '1',
                'readonly': True
            })
        }
