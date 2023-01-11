from django import forms
from django.forms import inlineformset_factory

from testing.models import TaskSetting, Cycle, OperatorNesting, Testing
from user.models import StudentGroup


class TestingForm(forms.ModelForm):
    title = forms.CharField(label='Наименование', widget=forms.TextInput(attrs={'name': 'title'}))
    student_group = forms.ModelChoiceField(label='Группы студентов',
                                           widget=forms.Select(attrs={'name': 'student_group'}),
                                           queryset=StudentGroup.objects.all())

    class Meta:
        model = Testing
        fields = ('title', 'student_group')


class TaskSettingForm(forms.ModelForm):
    weight = forms.IntegerField(label='Вес')

    be_present = TaskSetting.IsOperator.be_present
    absent = TaskSetting.IsOperator.absent
    choices_is_operator = (
        (be_present, be_present),
        (absent, absent)
    )
    is_if_operator = forms.ChoiceField(label='Наличие оператора if', widget=forms.RadioSelect,
                                       choices=choices_is_operator
                                       )

    simple = TaskSetting.Condition.simple
    composite = TaskSetting.Condition.composite
    choices_condition_operator = (
        (simple, simple),
        (composite, composite)
    )
    condition_of_if_operator = forms.ChoiceField(label='Условие оператора if', widget=forms.RadioSelect,
                                                 choices=choices_condition_operator)
    availability_of_cycles = forms.ModelMultipleChoiceField(label='Наличие цикла',
                                                            widget=forms.CheckboxSelectMultiple,
                                                            to_field_name="title",
                                                            queryset=Cycle.objects.all())
    cycle_condition = forms.ChoiceField(label='Условие цикла', widget=forms.RadioSelect,
                                        choices=choices_condition_operator
                                        )
    operator_nesting = forms.ModelMultipleChoiceField(label='Вложенность операторов',
                                                      widget=forms.CheckboxSelectMultiple,
                                                      to_field_name="title",
                                                      queryset=OperatorNesting.objects.all())

    class Meta:
        model = TaskSetting
        fields = '__all__'
        exclude = ['user', 'testing']


TaskSettingFormSet = inlineformset_factory(
    Testing,
    TaskSetting,
    form=TaskSettingForm,
    min_num=1,  # минимальное количество форм, которые необходимо заполнить
    extra=1,  # количество пустых форм для отображения
    can_delete=False  # показать флажок в каждой форме, чтобы удалить строку
)
