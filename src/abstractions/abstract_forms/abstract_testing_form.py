from django import forms

from apps.user.models import StudentGroup


class AbstractTestingForm(forms.ModelForm):
    student_groups = forms.ModelMultipleChoiceField(
        label='Группы студентов',
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'name': 'student_group',
            }
        ),
        queryset=StudentGroup.objects.all()
    )

    class Meta:
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
            'task_lead_time': forms.TimeInput(attrs={
                'class': 'uk-margin-small uk-input uk-width-small',
                'type': 'time'
            })
        }
