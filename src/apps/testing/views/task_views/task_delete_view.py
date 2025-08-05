from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.testing.abstractions.abstract_views import AbstractTaskView
from apps.testing.models import Testing
from mixins import LoginMixin


class TaskDeleteView(AbstractTaskView, LoginMixin, DeleteView):
    def form_valid(self, form) -> HttpResponseRedirect:
        super().form_valid(form)
        self._update_serial_number_tasks()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def _update_serial_number_tasks(self) -> None:
        testing = Testing.objects.get(id=self.request.GET['testing_pk'])
        tasks = testing.task_set.all()
        for index, task in enumerate(tasks, start=1):
            task.serial_number = index
            task.save()

    def get_success_url(self) -> reverse_lazy:
        return reverse_lazy(f'testing:teacher_testing_detail', kwargs={'pk': self.request.GET['testing_pk']})
