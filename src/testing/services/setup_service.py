from django.db.models import Manager
from django.forms import Form

from testing.models import TaskSetup
from testing.services.filter_task_setup import FilterSetup
from user.models import User


class SetupService:
    user: User
    setup: Manager[TaskSetup]
    setup_form: Manager[Form]
    setup_filter: Manager[FilterSetup]

    def __init__(self, user: User, setup_form):
        self.user = user
        self.setup = TaskSetup.objects
        self.setup_form = setup_form

    def set(self) -> None:
        filtered_setup = self.filter()
        if filtered_setup.exists():
            self._set_for_user(filtered_setup)
        else:
            self.add()

    def _set_for_user(self, filtered_setup: Manager[FilterSetup]) -> None:
        filtered_setup = filtered_setup.filter(users=self.user)
        if filtered_setup.exists():
            self.setup = filtered_setup.first()
        else:
            self.setup.users.add(self.user)

    def filter(self) -> Manager[FilterSetup]:
        filter_setup = FilterSetup(self.setup, self.setup_form)
        filtered_setup = filter_setup.execute()
        self.setup = filtered_setup.first()
        return filtered_setup

    def add(self) -> None:
        self.setup = self.setup_form.save(commit=False)
        self.setup.pk = None
        self.setup.save()
        self.setup_form.save_m2m()
        self.setup.users.add(self.user)

    @staticmethod
    def update(task: Manager, setup: Manager) -> Manager:
        task.task_setup = setup
        task.save(update_fields=['task_setup'])
        return task

    def get(self):
        return self.setup

    def get_pk(self):
        return self.setup.pk

    def get_form(self):
        return self.setup_form
