from django.db.models import F, Q
from django.forms import ModelMultipleChoiceField

from testing.models import *


# TODO Проверить дубликат self.task_setup.filter(**self.task_setups_fields).
#  Подумать насчёт task (self.task)
#  Посмотреть фильтрацию task_filter может её в init?
class TaskService:
    user: str = None
    task_form = None
    task = None
    task_filter = None
    task_setup_form = None
    task_setup = None
    weight = None
    task_setups_fields = {}
    testing = None
    pk = None
    task_setup_filter = None
    q_obj: Q = None

    def __init__(self, user, forms, testing):
        self.user = user
        self.task = Task.objects
        self.task_setup = TaskSetup.objects
        self.task_form = forms['task_form']
        self.task_setup_form = forms['task_setup_form']
        self.weight = self.task_form.cleaned_data['weight']
        self.filter_fields()
        self.testing = testing

    def filter_fields(self):
        self.task_setup_filter = self.task_setup
        self.q_obj = Q()
        for field_name, field in self.task_setup_form.fields.items():
            self.filter_field(field_name, field)
        self.task_setup_filter = self.task_setup_filter.filter(self.q_obj)

    def filter_field(self, field_name, field):
        if isinstance(field, ModelMultipleChoiceField):
            self.filter_many_to_many_fields(field_name, field)
        else:
            q_filter = {
                f'{field_name}': self.task_setup_form.cleaned_data[field_name]}
            self.q_obj &= Q(**q_filter)

    def filter_many_to_many_fields(self, field_name, field):
        excluded_choices = [choice[1] for choice in field.choices]
        for item in self.task_setup_form.cleaned_data[field_name]:
            item_filter = {f'{field_name}__title': item.title}
            self.task_setup_filter = self.task_setup_filter.filter(
                **item_filter)
            excluded_choices.remove(f'{item}')
        if excluded_choices:
            self.filter_excluded_many_to_many_fields(
                field_name,
                excluded_choices
            )

    def filter_excluded_many_to_many_fields(self, field_name,
                                            excluded_choices):
        for excluded_choice in excluded_choices:
            excluded_choice_filter = {f'{field_name}__title': excluded_choice}
            self.task_setup_filter = self.task_setup_filter.exclude(
                **excluded_choice_filter
            )

    def add(self) -> None:
        """Добавляет задачу Task"""
        self.set_task_setup()
        self.create_or_increase()

    def set_task_setup(self):
        if self.task_setup_filter.exists():
            task_setup = self.task_setup_filter.filter(users=self.user)
            if task_setup.exists():
                self.task_setup = task_setup.first()
            else:
                self.task_setup.first().users.add(self.user)
                self.task_setup = self.task_setup.first()
        else:
            self.create_task_setup()

    def create_task_setup(self):
        self.task_setup = self.task_setup_form.save(commit=False)
        self.task_setup.pk = None
        self.task_setup.save()
        self.task_setup_form.save_m2m()
        self.task_setup.users.add(self.user)

    def create_or_increase(self):
        self.task_filter = self.task.filter(
            weight=self.weight,
            testing=self.testing,
            task_setup=self.task_setup
        )
        if self.task_filter.exists():
            self.increase_count(self.task_filter)
        else:
            self.create()

    def increase_count(self, task):
        task.update(count=F('count') + 1)
        self.pk = task.first().pk

    def create(self):
        self.task = self.task.create(
            weight=self.weight,
            testing=self.testing,
            task_setup=self.task_setup,
            count=1
        )
        self.pk = self.task.pk

    def update(self, task):
        if self.task_setup_form.changed_data:
            if task.count == 1:
                self.update_non_recurring(task)
            else:
                task.count -= 1
                task.save(update_fields=['count'])
                self.add()

    def update_non_recurring(self, task):
        self.update_weight(task)
        if self.task_setup_filter.exists():
            self.task_setup = self.task_setup_filter.first()
            self.task_filter = self.task.filter(
                weight=self.weight,
                testing=self.testing,
                task_setup=self.task_setup
            )
            if self.task_filter.exists():
                task.delete()
                task = self.task_filter
                self.increase_count(task)
                self.pk = task.first().pk
            else:
                update_task_setup(task, self.task_setup)
                self.pk = task.pk
        else:
            task.delete()
            self.add()

    def update_weight(self, task):
        if self.task_form.changed_data:
            task.weight = self.task_form.cleaned_data['weight']
            task.save(update_fields=['weight'])

    def get_pk(self):
        return self.pk


def update_task_setup(task, task_setup):
    task.task_setup = task_setup
    task.save(update_fields=['task_setup'])
