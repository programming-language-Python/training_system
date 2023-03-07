from django.db.models import F

from testing.models import *
from testing.services.filter import filter_many_to_many_relationship


class TaskManager:
    def __init__(self, user, forms, testing):
        self.user = user
        self.task_form = forms['task_form']
        self.task_setup_form = forms['task_setup_form']
        self.testing = testing
        self.pk = None

    def add(self):
        """Добавляет задачу Task"""
        task_setup = self.get_task_setup()
        self.create(task_setup)

    def create(self, task_setup):
        weight = self.task_form.cleaned_data['weight']
        task = Task.objects.filter(weight=weight,
                                   testing=self.testing,
                                   task_setup=task_setup)
        if task.exists():
            task.update(count=F('count') + 1)
            self.pk = task.first().pk
        else:
            task = Task.objects.create(weight=weight,
                                       testing=self.testing,
                                       task_setup=task_setup,
                                       count=1)
            self.pk = task.pk

    def get_task_setup(self):
        filtered_task_setup = self.get_filtered_setup_task()
        if filtered_task_setup.exists():
            filtered_task_setup_by_user = filtered_task_setup.filter(users=self.user)
            if filtered_task_setup_by_user.exists():
                return filtered_task_setup.first()
            return filtered_task_setup
        return self.create_task_setup()

    def get_filtered_setup_task(self):
        filtered_many_to_many_relationship = self.get_filtered_many_to_many_relationship()
        is_if_operator = self.task_setup_form.cleaned_data['is_if_operator']
        condition_of_if_operator = self.task_setup_form.cleaned_data['condition_of_if_operator']
        cycle_condition = self.task_setup_form.cleaned_data['cycle_condition']
        filtered_task_setup = filtered_many_to_many_relationship.filter(
            is_if_operator=is_if_operator,
            condition_of_if_operator=condition_of_if_operator,
            cycle_condition=cycle_condition
        )
        return filtered_task_setup

    def get_filtered_many_to_many_relationship(self):
        obj_to_filter = filter_many_to_many_relationship(
            items_model=Cycle,
            form=self.task_setup_form,
            filter_field='presence_one_of_cycles'
        )
        filtered_many_to_many_relationship = filter_many_to_many_relationship(
            items_model=OperatorNesting,
            obj_to_filter=obj_to_filter,
            form=self.task_setup_form,
            filter_field='operator_nesting'
        )
        return filtered_many_to_many_relationship

    def create_task_setup(self):
        task_setup = self.task_setup_form.save(commit=False)
        task_setup.pk = None
        task_setup.save()
        self.task_setup_form.save_m2m()
        task_setup.users.add(self.user)
        return task_setup

    # проверить
    # не работает
    # print('not filtered_task_setup.exists() is_task_repeated')

    # работает
    # print('not filtered_task_setup.exists() not is_task_repeated')
    def update(self, task):
        # self.block_fields()
        if task.count == 1:
            self.update_non_recurring(task)
        else:
            task.count -= 1
            task.save(update_fields=['count'])
            self.add()

    def block_fields(self):
        is_if_operator_absent = self.task_setup_form.cleaned_data['is_if_operator'] == 'Отсутствует'
        is_empty_presence_one_of_cycles = self.task_setup_form.cleaned_data['presence_one_of_cycles'] == ''
        if is_if_operator_absent:
            self.task_setup_form.cleaned_data['condition_of_if_operator'] = ''
        if is_empty_presence_one_of_cycles:
            self.task_setup_form.cleaned_data['cycle_condition'] = ''

    def update_non_recurring(self, task):
        self.update_weight(task)
        filtered_task_setup = self.get_filtered_setup_task()
        is_exists_and_changed_data = filtered_task_setup.exists() and self.task_setup_form.changed_data
        if is_exists_and_changed_data:
            task_setup = filtered_task_setup.first()
        else:
            task_setup = self.get_task_setup()
        update_task_setup(task, task_setup)
        self.pk = task.pk

    def update_weight(self, task):
        if self.task_form.changed_data:
            task.weight = self.task_form.cleaned_data['weight']
            task.save(update_fields=['weight'])

    # def update_quantity_and_add_task(self, task):
    #     task.count -= 1
    #     task.save(update_fields=['count'])
    #     self.add()


def update_task_setup(task, task_setup):
    task.task_setup = task_setup
    task.save(update_fields=['task_setup'])
