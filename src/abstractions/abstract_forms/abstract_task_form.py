from django import forms


class AbstractTaskForm(forms.ModelForm):
    weight = forms.IntegerField(
        label='Вес',
        widget=forms.NumberInput(
            attrs={
                'class': 'uk-input uk-form-width-small uk-form-small',
                'min': 1,
                'value': 1
            }
        )
    )
