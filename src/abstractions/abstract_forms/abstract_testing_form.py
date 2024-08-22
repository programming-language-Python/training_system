from django import forms

from apps.user.models import StudentGroup


class AbstractTestingForm(forms.ModelForm):
    title = forms.CharField(
        label='Наименование',
        widget=forms.TextInput(
            attrs={
                'class': 'uk-margin uk-input uk-form-width-medium',
                'name': 'title',
            }
        )
    )
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
    is_published = forms.BooleanField(
        label='Опубликовано',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_review_of_result_by_student = forms.BooleanField(
        label='Просмотр результата студентом',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_established_order_tasks = forms.BooleanField(
        label='Установленный порядок задач',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    task_lead_time = forms.TimeField(
        label='Время выполнения задачи',
        required=False,
        widget=forms.TimeInput(
            attrs={
                'class': 'uk-margin-small uk-input uk-width-small',
                'type': 'time'
            }
        )
    )
