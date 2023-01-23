from testing.models import *
from testing.services.filter import filter_many_to_many_relationship


class Task:
    def __init__(self, user, form, testing):
        self.user = user
        self.form = form
        self.task_setup_id = ''
        self.testing = testing

    def add(self):
        """Добавляет настройку задачи TaskSetup"""
        filtered_task_setup = self.get_filter()
        is_exists = filtered_task_setup.exists()
        if is_exists:
            self.create_testing(filtered_task_setup.first())
            return
        self.create_testing_and_task_setup()

    def create_testing_and_task_setup(self):
        task_setup = self.create_task_setup()
        self.create_testing(task_setup)

    def create_task_setup(self):
        task_setup = self.form.save(commit=False)
        task_setup.save()
        task_setup.user.add(self.user)
        self.form.save_m2m()
        return task_setup

    def create_testing(self, task_setup):
        student_groups = self.testing.student_group.all()
        self.testing.pk = None
        self.testing.task_setup = task_setup
        self.testing.save()

        for student_group in student_groups:
            self.testing.student_group.add(student_group)

        self.task_setup_id = task_setup.id

    def update_testing(self):
        pass

    def get_filter(self):
        filtered_many_to_many_relationship = self.get_filtered_many_to_many_relationship()
        weight = self.form.cleaned_data['weight']
        is_if_operator = self.form.cleaned_data['is_if_operator']
        condition_of_if_operator = self.form.cleaned_data['condition_of_if_operator']
        cycle_condition = self.form.cleaned_data['cycle_condition']
        filtered_task_setup = filtered_many_to_many_relationship.filter(
            weight=weight,
            is_if_operator=is_if_operator,
            condition_of_if_operator=condition_of_if_operator,
            cycle_condition=cycle_condition
        )
        return filtered_task_setup

    def get_filtered_many_to_many_relationship(self):
        obj_to_filter = TaskSetup.objects.filter(user=self.user)
        obj_to_filter = filter_many_to_many_relationship(
            items_model=Cycle,
            obj_to_filter=obj_to_filter,
            form=self.form,
            filter_field='availability_of_cycles'
        )
        filtered_many_to_many_relationship = filter_many_to_many_relationship(
            items_model=OperatorNesting,
            obj_to_filter=obj_to_filter,
            form=self.form,
            filter_field='operator_nesting'
        )
        return filtered_many_to_many_relationship
