from typing import Type

from django.db.models import Model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import DeleteView


class AbstractTestingDeleteView(DeleteView):
    model: Type[Model]
    template_name = 'testing_confirm_delete.html'
    success_url: Type[reverse_lazy]

    def form_valid(self, form) -> HttpResponseRedirect:
        obj = self.get_object()
        if obj.is_solving_testing_set():
            obj.date_of_deletion = now()
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
