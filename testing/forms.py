from django import forms
from django.forms import inlineformset_factory

from testing.models import TaskSetting, Cycle, OperatorNesting, Testing
from user.models import StudentGroup


class TestingForm(forms.ModelForm):
    # title = forms.CharField(label='Наименование', attrs={'name': 'title'}, max_length=25)
    # student_group = forms.ModelChoiceField(label='Группы студентов', attrs={'name': 'student_group'},
    #                                        queryset=StudentGroup.objects.all())
    class Meta:
        model = Testing
        fields = ['title', 'student_group']
        widgets = {
            'title': forms.TextInput(attrs={'name': 'title'}),
            'student_group': forms.Select(attrs={'name': 'student_group'}),
        }


class TaskSettingForm(forms.ModelForm):
    class Meta:
        model = TaskSetting
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={'name': 'setting_title'}),
            'weight': forms.NumberInput(attrs={'name': 'setting_weight'}),
            'is_if_operator': forms.RadioSelect(attrs={'name': 'setting_is_if_operator'}),
            'condition_of_if_operator': forms.RadioSelect(attrs={'name': 'condition_of_if_operator'}),
            'availability_of_cycles': forms.CheckboxSelectMultiple(attrs={'name': 'availability_of_cycles'}),
            'cycle_condition': forms.RadioSelect(attrs={'name': 'cycle_condition'}),
            'operator_nesting': forms.CheckboxSelectMultiple(attrs={'name': 'operator_nesting'}),
        }

    # title_task_setting = forms.CharField(label='Наименование', max_length=25)
    # weight = forms.IntegerField(label='Вес')
    #
    # be_present = TaskSetting.IsOperator.be_present
    # absent = TaskSetting.IsOperator.absent
    # choices_is_operator = (
    #     (be_present, be_present),
    #     (absent, absent)
    # )
    # is_if_operator = forms.ChoiceField(label='Наличие оператора if', widget=forms.RadioSelect,
    #                                    choices=choices_is_operator
    #                                    )
    #
    # simple = TaskSetting.Condition.simple
    # composite = TaskSetting.Condition.composite
    # choices_condition_operator = (
    #     (simple, simple),
    #     (composite, composite)
    # )
    # condition_of_if_operator = forms.ChoiceField(label='Условие оператора if', widget=forms.RadioSelect,
    #                                              choices=choices_condition_operator)
    # availability_of_cycles = forms.ModelMultipleChoiceField(label='Наличие цикла',
    #                                                         widget=forms.CheckboxSelectMultiple,
    #                                                         to_field_name="title",
    #                                                         queryset=Cycle.objects.all())
    # cycle_condition = forms.ChoiceField(label='Условие цикла', widget=forms.RadioSelect,
    #                                     choices=choices_condition_operator
    #                                     )
    # operator_nesting = forms.ModelMultipleChoiceField(label='Вложенность операторов',
    #                                                   widget=forms.CheckboxSelectMultiple,
    #                                                   to_field_name="title",
    #                                                   queryset=OperatorNesting.objects.all())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(TaskSettingForm, self).__init__(*args, **kwargs)
        self.fields['is_if_operator'].initsial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['test_{index}'.format(index=index)] = \
                forms.CharField()


TaskSettingFormSet = inlineformset_factory(
    TaskSetting,
    Testing,
    form=TaskSettingForm,
    min_num=2,  # минимальное количество форм, которые необходимо заполнить
    extra=1,  # количество пустых форм для отображения
    can_delete=False  # показать флажок в каждой форме, чтобы удалить строку
)
