from django import forms

from testing.models import Setting, Cycle, OperatorNesting, Testing, Task
from user.models import StudentGroup

CLASS_UK_SELECT = 'uk-select'
CLASS_UK_FORM_WIDTH_SMALL = 'uk-form-width-small'
SELECT_TAG_CLASSES = f'{CLASS_UK_SELECT} {CLASS_UK_FORM_WIDTH_SMALL}'


class TestingForm(forms.ModelForm):
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

    class Meta:
        model = Testing
        fields = (
            'title',
            'student_groups',
            'is_published',
            'is_review_of_result_by_student'
        )


class TaskForm(forms.ModelForm):
    weight = forms.IntegerField(
        label='Вес',
        widget=forms.NumberInput(
            attrs={
                'class': 'uk-input uk-form-width-small uk-form-small',
                'value': 1
            }
        )
    )

    class Meta:
        model = Task
        fields = ('weight',)


class SettingForm(forms.ModelForm):
    BE_PRESENT = 'Присутствует'
    ABSENT = 'Отсутствует'
    choices_is_operator = (
        (BE_PRESENT, BE_PRESENT),
        (ABSENT, ABSENT)
    )
    is_if_operator = forms.ChoiceField(
        label='Наличие оператора if',
        widget=forms.Select(
            attrs={
                'class': SELECT_TAG_CLASSES
            }
        ),
        choices=choices_is_operator
    )

    SIMPLE = 'Простое'
    COMPOSITE = 'Составное'
    choices_condition_operator = (
        ('', '----'),
        (SIMPLE, SIMPLE),
        (COMPOSITE, COMPOSITE)
    )
    condition_of_if_operator = forms.ChoiceField(
        label='Условие оператора if',
        required=False,
        initial=choices_condition_operator[1],
        widget=forms.Select(
            attrs={
                'class': SELECT_TAG_CLASSES
            }
        ),
        choices=choices_condition_operator
    )
    cycle = forms.ModelMultipleChoiceField(
        label='Цикл',
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        to_field_name='title',
        queryset=Cycle.objects.all()
    )
    cycle_condition = forms.ChoiceField(
        label='Условие цикла',
        required=False,
        initial=choices_condition_operator[1],
        widget=forms.Select(
            attrs={
                'class': SELECT_TAG_CLASSES
            }
        ),
        choices=choices_condition_operator
    )
    operator_nesting = forms.ModelMultipleChoiceField(
        label='Вложенность операторов',
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        to_field_name='title',
        queryset=OperatorNesting.objects.all()
    )
    is_OOP = forms.CheckboxInput()
    is_strings = forms.CheckboxInput()

    class Meta:
        model = Setting
        fields = '__all__'
        exclude = ['users', 'testing']
