from django.db.models import F

from testing.models import *
from testing.services.filter import filter_many_to_many_relationship


class TaskManager:
    user = None
    task_form = None
    task = None
    task_setup_form = None
    task_setup = None
    weight = None
    is_OOP = None
    is_if_operator = None
    condition_of_if_operator = None
    cycle_condition = None
    testing = None
    pk = None

    def __init__(self, user, forms, testing):
        self.user = user
        self.task_form = forms['task_form']
        self.task = Task.objects
        self.task_setup_form = forms['task_setup_form']
        self.task_setup = TaskSetup.objects
        self.weight = self.task_form.cleaned_data['weight']
        self.is_if_operator = self.task_setup_form.cleaned_data['is_if_operator']
        self.condition_of_if_operator = self.task_setup_form.cleaned_data['condition_of_if_operator']
        self.cycle_condition = self.task_setup_form.cleaned_data['cycle_condition']
        self.is_OOP = self.task_setup_form.cleaned_data['is_OOP']
        self.is_strings = self.task_setup_form.cleaned_data['is_strings']
        self.testing = testing

    def add(self):
        """Добавляет задачу Task"""
        self.create_or_set_task_setup()
        self.create_or_increase()

    def create_or_increase(self):
        self.task = self.task.filter(weight=self.weight,
                                     testing=self.testing,
                                     task_setup=self.task_setup)
        if self.task.exists():
            self.increase_count()
        else:
            self.create()

    def increase_count(self):
        self.task.update(count=F('count') + 1)
        self.pk = self.task.first().pk

    def create(self):
        self.task = self.task.create(weight=self.weight,
                                     testing=self.testing,
                                     task_setup=self.task_setup,
                                     count=1)
        self.pk = self.task.pk

    def create_or_set_task_setup(self):
        self.task_setup = self.task_setup.filter(is_strings=self.is_strings)
        is_not_created_strings = not self.task_setup.exists() and self.is_strings is True
        if is_not_created_strings:
            return self.create_task_setup()
        self.task_setup = self.task_setup.filter(is_OOP=self.is_OOP)
        is_not_created_OOP = not self.task_setup.exists() and self.is_OOP is True
        if is_not_created_OOP:
            return self.create_task_setup()
        self.task_setup = self.task_setup.filter(
            is_if_operator=self.is_if_operator,
            condition_of_if_operator=self.condition_of_if_operator,
            cycle_condition=self.cycle_condition)
        if not self.task_setup.exists():
            return self.create_task_setup()
        self.task_setup = filter_many_to_many_relationship(
            items_model=Cycle,
            obj_to_filter=self.task_setup,
            form=self.task_setup_form,
            filter_field='presence_one_of_cycles')
        if not self.task_setup.exists():
            return self.create_task_setup()
        self.task_setup = filter_many_to_many_relationship(
            items_model=OperatorNesting,
            obj_to_filter=self.task_setup,
            form=self.task_setup_form,
            filter_field='operator_nesting')
        if not self.task_setup.exists():
            return self.create_task_setup()
        task_setup = self.task_setup.filter(users=self.user)
        if task_setup.exists():
            self.task_setup = task_setup.first()
        else:
            self.task_setup.first().users.add(self.user)
            self.task_setup = self.task_setup.first()

    def get_task_setup(self):
        filtered_task_setup = self.get_filtered_setup_task()
        if filtered_task_setup.exists():
            filtered_task_setup_by_user = filtered_task_setup.filter(users=self.user)
            if filtered_task_setup_by_user.exists():
                return filtered_task_setup.first()
            return filtered_task_setup
        return self.create_task_setup()

    def get_filtered_setup_task(self):
        # is_if_operator = self.task_setup_form.cleaned_data['is_if_operator']
        # condition_of_if_operator = self.task_setup_form.cleaned_data['condition_of_if_operator']
        # cycle_condition = self.task_setup_form.cleaned_data['cycle_condition']
        # filtered_task_setup = TaskSetup.objects.filter(
        #     is_if_operator=is_if_operator,
        #     condition_of_if_operator=condition_of_if_operator,
        #     cycle_condition=cycle_condition
        # )
        filtered_task_setup = TaskSetup.objects.filter(
            is_strings=self.is_strings,
            is_OOP=self.is_OOP,
            is_if_operator=self.is_if_operator,
            condition_of_if_operator=self.condition_of_if_operator,
            cycle_condition=self.cycle_condition
        )
        filtered_task_setup = self.get_filtered_many_to_many_relationship(filtered_task_setup)
        return filtered_task_setup

    def get_filtered_many_to_many_relationship(self, obj_to_filter):
        obj_to_filter = filter_many_to_many_relationship(
            items_model=Cycle,
            obj_to_filter=obj_to_filter,
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
        self.task_setup = self.task_setup_form.save(commit=False)
        self.task_setup.pk = None
        self.task_setup.save()
        self.task_setup_form.save_m2m()
        self.task_setup.users.add(self.user)

    def update(self, task):
        if task.count == 1:
            print('1')
            self.update_non_recurring(task)
        else:
            print('>1')
            task.count -= 1
            task.save(update_fields=['count'])
            self.add()

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
