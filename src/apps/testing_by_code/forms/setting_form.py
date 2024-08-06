from django import forms

from apps.testing_by_code.models import OperatorNesting, Cycle, Setting
from apps.testing_by_code.types import ConditionType

CLASS_UK_SELECT = 'uk-select'
CLASS_UK_FORM_WIDTH_SMALL = 'uk-form-width-small'
SELECT_TAG_CLASSES = f'{CLASS_UK_SELECT} {CLASS_UK_FORM_WIDTH_SMALL}'


class SettingForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        is_if_operator = cleaned_data.get('is_if_operator')
        cycle = cleaned_data.get('cycle')
        is_OOP = cleaned_data.get('is_OOP')
        is_strings = cleaned_data.get('is_strings')

        # is_absent_if_operator = is_if_operator == OperatorPresenceType.ABSENT
        # if is_if_operator:
        #     cleaned_data['condition_of_if_operator'] = ConditionType.SIMPLE
        if cycle:
            cleaned_data['cycle_condition'] = ConditionType.SIMPLE
        is_lock_nesting_of_operators = is_if_operator or not cycle
        if is_lock_nesting_of_operators:
            cleaned_data['operator_nesting'] = OperatorNesting.objects.none()
        if is_OOP:
            cleaned_data = self._set_default_basic_fields(cleaned_data)
            cleaned_data['is_strings'] = False
        if is_strings:
            cleaned_data = self._set_default_basic_fields(cleaned_data)
            cleaned_data['is_OOP'] = False

    @staticmethod
    def _set_default_basic_fields(cleaned_data: dict) -> dict:
        cleaned_data['is_if_operator'] = True
        cleaned_data['condition_of_if_operator'] = ConditionType.SIMPLE
        cleaned_data['cycle'] = Cycle.objects.none()
        cleaned_data['cycle_condition'] = ConditionType.SIMPLE
        cleaned_data['operator_nesting'] = OperatorNesting.objects.none()
        return cleaned_data

    class Meta:
        model = Setting
        fields = '__all__'
        exclude = ['users', 'testing_by_code']
