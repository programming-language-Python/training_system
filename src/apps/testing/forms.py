from django import forms
from django.forms import formset_factory

from abstractions.abstract_form_fields.abstract_form_field_description import AbstractFormFieldDescription
from abstractions.abstract_forms import AbstractTestingForm, AbstractTaskForm
from apps.testing.constants import MIN_ASSESSMENT_THRESHOLD, MAX_ASSESSMENT_THRESHOLD
from apps.testing.models import Testing
from apps.testing.models.tasks.closed_question import AnswerOption, ClosedQuestion


class TestingForm(AbstractTestingForm):
    CLASS = 'uk-margin uk-input uk-form-width-medium'
    testing_meta = Testing._meta
    number = forms.IntegerField(
        label=testing_meta.get_field('number').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
            }
        )
    )
    likelihood_guessing_answers = forms.FloatField(
        label=testing_meta.get_field('likelihood_guessing_answers').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
                'max': MIN_ASSESSMENT_THRESHOLD,
                'min': 0,
                'step': '0.01'
            }
        )
    )
    assessment_threshold = forms.IntegerField(
        label=testing_meta.get_field('assessment_threshold').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': CLASS,
                'min': MIN_ASSESSMENT_THRESHOLD,
                'max': MAX_ASSESSMENT_THRESHOLD,
            }
        )
    )
    is_established_order_tasks = forms.BooleanField(
        label=testing_meta.get_field('is_established_order_tasks').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    task_lead_time = forms.TimeField(
        label=testing_meta.get_field('task_lead_time').verbose_name,
        widget=forms.TimeInput(
            attrs={
                'class': CLASS,
                'type': 'time'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        student_groups_value = self.fields.pop('student_groups')
        self.fields['student_groups'] = student_groups_value

    class Meta:
        model = Testing
        fields = '__all__'
        exclude = ['user', ]


class ClosedQuestionForm(AbstractTaskForm, AbstractFormFieldDescription):
    closed_question_meta = ClosedQuestion._meta
    is_several_correct_answers = forms.BooleanField(
        label=closed_question_meta.get_field('is_several_correct_answers').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_random_order_answer_options = forms.BooleanField(
        label=closed_question_meta.get_field('is_random_order_answer_options').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_partially_correct_execution = forms.BooleanField(
        label=closed_question_meta.get_field('is_partially_correct_execution').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )

    class Meta:
        model = ClosedQuestion
        fields = '__all__'
        exclude = ['testing', ]


class AnswerOptionForm(forms.ModelForm):
    answer_option_meta = AnswerOption._meta
    serial_number = forms.IntegerField(
        label=answer_option_meta.get_field('serial_number').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': 'serial-number',
                'min': 1
            }
        )
    )
    description = forms.CharField(
        label=answer_option_meta.get_field('description').verbose_name,
        widget=forms.Textarea(
            attrs={
                'class': 'uk-textarea',
                'rows': '5'
            }
        )
    )
    photo = forms.ImageField(
        label=answer_option_meta.get_field('photo').verbose_name,
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'photo',
            }
        )
    )
    is_correct = forms.BooleanField(
        label=answer_option_meta.get_field('is_correct').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'is-correct uk-checkbox',
            }
        )
    )

    class Meta:
        model = AnswerOption
        fields = ('serial_number', 'description', 'photo', 'is_correct',)
        exclude = ['closed_question', ]


AnswerOptionFormSet = formset_factory(AnswerOptionForm, extra=2)
