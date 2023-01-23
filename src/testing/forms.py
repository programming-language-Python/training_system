from django import forms
from django.forms import inlineformset_factory

from testing.models import TaskSetup, Cycle, OperatorNesting, Testing
from user.models import StudentGroup


class TestingForm(forms.ModelForm):
    title = forms.CharField(label='Наименование',
                            widget=forms.TextInput(
                                attrs={'name': 'title'}
                            ))
    student_group = forms.ModelMultipleChoiceField(label='Группы студентов',
                                                   widget=forms.SelectMultiple(
                                                       attrs={'name': 'student_group'}
                                                   ),
                                                   queryset=StudentGroup.objects.all())

    class Meta:
        model = Testing
        fields = ('title', 'student_group')


class TaskSetupForm(forms.ModelForm):
    weight = forms.IntegerField(label='Вес')

    be_present = TaskSetup.IsOperator.be_present
    absent = TaskSetup.IsOperator.absent
    choices_is_operator = (
        (be_present, be_present),
        (absent, absent)
    )
    is_if_operator = forms.ChoiceField(label='Наличие оператора if',
                                       widget=forms.RadioSelect,
                                       choices=choices_is_operator)

    simple = TaskSetup.Condition.simple
    composite = TaskSetup.Condition.composite
    choices_condition_operator = (
        (simple, simple),
        (composite, composite)
    )
    condition_of_if_operator = forms.ChoiceField(label='Условие оператора if',
                                                 widget=forms.RadioSelect,
                                                 choices=choices_condition_operator)
    availability_of_cycles = forms.ModelMultipleChoiceField(label='Наличие цикла',
                                                            widget=forms.CheckboxSelectMultiple,
                                                            to_field_name='title',
                                                            required=False,
                                                            queryset=Cycle.objects.all())
    cycle_condition = forms.ChoiceField(label='Условие цикла',
                                        widget=forms.RadioSelect,
                                        choices=choices_condition_operator)
    operator_nesting = forms.ModelMultipleChoiceField(label='Вложенность операторов',
                                                      widget=forms.CheckboxSelectMultiple,
                                                      to_field_name='title',
                                                      required=False,
                                                      queryset=OperatorNesting.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super(TaskSetupForm, self).__init__(*args, **kwargs)
    #     self.fields['availability_of_cycles'].required = False
    #     self.fields['operator_nesting'].required = False

    class Meta:
        model = TaskSetup
        fields = '__all__'
        exclude = ['user', 'testing']


# TaskSetupFormSet = inlineformset_factory(
#     Testing,
#     TaskSetup,
#     form=TaskSetupForm,
#     min_num=1,  # минимальное количество форм, которые необходимо заполнить
#     extra=1,  # количество пустых форм для отображения
#     can_delete=False  # показать флажок в каждой форме, чтобы удалить строку
# )
