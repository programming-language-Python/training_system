from django.db.models import Manager
from django.forms import Form

from testing.models import TaskSetup
from testing.services.filter_task_setup import FilterSetup


class SetupService:
    setup: Manager[TaskSetup]
    setup_form: Manager[Form]
    setup_filter: Manager[FilterSetup]

    def __init__(self, setup_form):
        self.setup = TaskSetup.objects
        self.setup_form = setup_form
        self.setup_filter = self._filter_setup()

    def _filter_setup(self) -> Manager[FilterSetup]:
        filter_task = FilterSetup(self.setup, self.setup_form)
        return filter_task.execute()

    def set_setup(self) -> None:
        if self.setup_filter.exists():
            setup = self.setup_filter.filter(users=self.user)
            if setup.exists():
                self.setup = setup.first()
            else:
                self.setup.first().users.add(self.user)
                self.setup = self.setup.first()
        else:
            self.create()

    def create(self) -> None:
        self.setup = self.setup_form.save(commit=False)
        self.setup.pk = None
        self.setup.save()
        self.setup_form.save_m2m()
        self.setup.users.add(self.user)

    @staticmethod
    def update(task: Manager, setup: Manager) -> Manager:
        task.setup = setup
        task.save(update_fields=['setup'])
        return task
