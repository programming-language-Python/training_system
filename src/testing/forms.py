from django import forms

from testing.models import TaskSetup, Cycle, OperatorNesting, Testing, Task
from user.models import StudentGroup

class_uk_select = 'uk-select'
class_uk_form_width_small = 'uk-form-width-small'
select_tag_classes = f'{class_uk_select} {class_uk_form_width_small}'


class TestingForm(forms.ModelForm):
    title = forms.CharField(label='Наименование',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'uk-margin uk-input uk-form-width-medium',
                                    'name': 'title',
                                }
                            ))
    student_groups = forms.ModelMultipleChoiceField(label='Группы студентов',
                                                    widget=forms.CheckboxSelectMultiple(
                                                        attrs={
                                                            'name': 'student_group',
                                                        }
                                                    ),
                                                    queryset=StudentGroup.objects.all())
    is_published = forms.BooleanField(label='Опубликовано',
                                      required=False,
                                      widget=forms.CheckboxInput(
                                          attrs={
                                              'class': 'uk-checkbox'
                                          }
                                      ))

    class Meta:
        model = Testing
        fields = ('title', 'student_groups', 'is_published')


class TaskForm(forms.ModelForm):
    weight = forms.IntegerField(label='Вес',
                                widget=forms.NumberInput(
                                    attrs={
                                        'class': 'uk-input uk-form-width-small uk-form-small',
                                        'value': 1
                                    }
                                ))

    class Meta:
        model = Task
        fields = ('weight',)


class TaskSetupForm(forms.ModelForm):
    be_present = TaskSetup.IsOperator.be_present
    absent = TaskSetup.IsOperator.absent
    choices_is_operator = (
        (be_present, be_present),
        (absent, absent)
    )
    # use_of_all_variables = forms.CheckboxInput()
    is_if_operator = forms.ChoiceField(label='Наличие оператора if',
                                       widget=forms.Select(
                                           attrs={
                                               'class': select_tag_classes
                                           }
                                       ),
                                       choices=choices_is_operator)

    simple = TaskSetup.Condition.simple
    composite = TaskSetup.Condition.composite
    choices_condition_operator = (
        ('', '----'),
        (simple, simple),
        (composite, composite)
    )
    condition_of_if_operator = forms.ChoiceField(label='Условие оператора if',
                                                 required=False,
                                                 initial=choices_condition_operator[1],
                                                 widget=forms.Select(
                                                     attrs={
                                                         'class': select_tag_classes
                                                     }
                                                 ),
                                                 choices=choices_condition_operator)
    presence_one_of_cycles = forms.ModelMultipleChoiceField(label='Наличие одного из следующих циклов',
                                                            required=False,
                                                            widget=forms.CheckboxSelectMultiple(
                                                            ),
                                                            to_field_name='title',
                                                            queryset=Cycle.objects.all())
    cycle_condition = forms.ChoiceField(label='Условие цикла',
                                        required=False,
                                        initial=choices_condition_operator[1],
                                        widget=forms.Select(
                                            attrs={
                                                'class': select_tag_classes
                                            }
                                        ),
                                        choices=choices_condition_operator)
    operator_nesting = forms.ModelMultipleChoiceField(label='Вложенность операторов',
                                                      required=False,
                                                      widget=forms.CheckboxSelectMultiple(
                                                      ),
                                                      to_field_name='title',
                                                      queryset=OperatorNesting.objects.all())
    is_OOP = forms.CheckboxInput()
    is_strings = forms.CheckboxInput()

    class Meta:
        model = TaskSetup
        fields = '__all__'
        exclude = ['users', 'testing']

# TaskSetupFormSet = inlineformset_factory(
#     Testing,
#     TaskSetup,
#     form=TaskSetupForm,
#     min_num=1,  # минимальное количество форм, которые необходимо заполнить
#     extra=1,  # количество пустых форм для отображения
#     can_delete=False  # показать флажок в каждой форме, чтобы удалить строку
# )
