from django.db.models import F

from testing.models import *
from testing.services.filter import filter_many_to_many_relationship


class TaskManager:
    def __init__(self, user, form, testing=''):
        self.user = user
        self.form = form
        self.testing = testing
        self.id = ''

    def add(self):
        """Добавляет задачу Task"""
        filtered_task_setup = self.get_filter()
        if filtered_task_setup.exists():
            self.create_task(filtered_task_setup.first())
        else:
            self.create_task_setup_and_task()

    def create_task_setup_and_task(self):
        task_setup_created = self.create_task_setup()
        self.create_task(task_setup_created)

    def create_task_setup(self):
        task_setup = self.form.save(commit=False)
        task_setup.save()
        task_setup.user.add(self.user)
        self.form.save_m2m()
        return task_setup

    # нужна?
    def create_task(self, task_setup):
        task = Task.objects.filter(testing=self.testing,
                                   task_setup=task_setup)
        if task.exists():
            task.update(count=F('count') + 1)
            self.id = task.first().id
        else:
            task = Task.objects.create(testing=self.testing,
                                       task_setup=task_setup,
                                       count=1)
            self.id = task.id

    def update(self, task):
        self.testing = task.testing
        filtered_task_setup = self.get_filter()
        is_task_repeated = task.count > 1
        if filtered_task_setup.exists():
            if is_task_repeated:
                # проверено всё работает :)
                print('filtered_task_setup.exists() is_task_repeated')
                # дубль 1
                task.count -= 1
                task.save(update_fields=['count'])
                self.create_task(filtered_task_setup.first())
            else:
                # проверено всё работает :)
                print('filtered_task_setup.exists() not is_task_repeated')
                task.delete()
                self.create_task(filtered_task_setup.first())
        else:
            if is_task_repeated:
                # добавляет дубль task_setup как новый и меняет дубли task. В итоге дубли task становятся одинаковыми
                print('not filtered_task_setup.exists() is_task_repeated')
                # дубль 1
                task.count -= 1
                task.save(update_fields=['count'])
                # created_task_setup = self.create_task_setup()
                # Task.objects.create(testing=self.testing,
                #                     task_setup=created_task_setup,
                #                     count=1)
                self.create_task_setup_and_task()
            else:
                # если нет настройки задачи task_setup и задачи task
                print('not filtered_task_setup.exists() not is_task_repeated')
                task_setup_created = self.create_task_setup()
                task.task_setup = task_setup_created
                task.save(update_fields=['task_setup'])
                # task.update(task_setup=task_setup_created)

    # def update_quantity_and_add_task(self, task):
    #     task.count -= 1
    #     task.save(update_fields=['count'])
    #     self.add()

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
