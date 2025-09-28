from django import forms


class AbstractSolvingTaskForm(forms.ModelForm):
    answer = forms.CharField(
        label='Ответ',
        required=False,
        widget=forms.TextInput()
    )

    class Meta:
        fields = ('time_left', 'answer',)
        widgets = {
            'time_left': forms.TextInput(attrs={
                'class': 'uk-margin-small uk-input uk-width-small',
                'type': 'text',
                'tabindex': '1',
                'readonly': True
            })
        }
