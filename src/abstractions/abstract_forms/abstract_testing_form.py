from django import forms


class AbstractTestingForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        lead_time = cleaned_data.get('lead_time')
        if lead_time:
            cleaned_data['task_lead_time'] = None

    class Meta:
        field_time = forms.TimeInput(attrs={
            'class': 'uk-margin-small uk-input uk-width-small',
            'type': 'time'
        })
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'uk-margin uk-input uk-form-width-medium',
                'name': 'title'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'uk-checkbox'
            }),
            'is_review_of_result_by_student': forms.CheckboxInput(attrs={
                'class': 'uk-checkbox'
            }),
            'is_established_order_tasks': forms.CheckboxInput(attrs={
                'class': 'uk-checkbox'
            }),
            'lead_time': field_time,
            'task_lead_time': field_time
        }
