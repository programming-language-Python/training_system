from django.db.models import F

from testing.models import *
from testing.services.filter import filter_many_to_many_relationship


class TaskManager:
    def __init__(self, user, form, testing):
        self.user = user
        self.form = form
        self.testing = testing
        self.pk = None

    def add(self):
        """Добавляет задачу Task"""
        task_setup = self.get_task_setup()
        self.create(task_setup)

    def create(self, task_setup):
        task = Task.objects.filter(testing=self.testing,
                                   task_setup=task_setup)
        if task.exists():
            task.update(count=F('count') + 1)
            self.pk = task.first().pk
        else:
            task = Task.objects.create(testing=self.testing,
                                       task_setup=task_setup,
                                       count=1)
            self.pk = task.pk

    def get_task_setup(self):
        filtered_task_setup = self.get_filter()
        if filtered_task_setup.exists():
            print('filtered_task_setup.exists')
            return filtered_task_setup.first()
        return self.create_task_setup()

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

    def create_task_setup(self):
        task_setup = self.form.save(commit=False)
        task_setup.pk = None
        task_setup.save()
        task_setup.user.add(self.user)
        self.form.save_m2m()
        return task_setup

    # проверить
    # не работает
    # print('not filtered_task_setup.exists() is_task_repeated')

    # работает
    # print('not filtered_task_setup.exists() not is_task_repeated')
    def update(self, task):
        if task.count == 1:
            print('1')
            filtered_task_setup = self.get_filter()
            if filtered_task_setup.exists():
                # работает
                print('update filtered_task_setup.exists()')
                task.delete()
                self.create(filtered_task_setup.first())
            else:
                print('update not filtered_task_setup.exists()')
                # работает
                # print('not filtered_task_setup.exists() not is_task_repeated')
                task.task_setup = self.get_task_setup()
                task.save(update_fields=['task_setup'])
                self.pk = task.pk
            # # print('not filtered_task_setup.exists() is_task_repeated')
            # task.count -= 1
            # task.save(update_fields=['count'])
            #
            # task.task_setup = self.get_task_setup()
            # task.save(update_fields=['task_setup'])

            # # работает
            # # print('not filtered_task_setup.exists() not is_task_repeated')
            # task.task_setup = self.get_task_setup()
            # task.save(update_fields=['task_setup'])
            # self.pk = task.pk
        else:
            print('all')
            task.count -= 1
            task.save(update_fields=['count'])
            self.add()

    # def update_quantity_and_add_task(self, task):
    #     task.count -= 1
    #     task.save(update_fields=['count'])
    #     self.add()
