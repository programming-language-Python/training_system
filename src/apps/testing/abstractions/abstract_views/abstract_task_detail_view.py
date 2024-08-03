from typing import MutableMapping

from django.db.models import Model
from django.views.generic import DetailView


class AbstractTaskDetailView(DetailView):
    model: Model
    context_object_name = 'task'
    template_name: str

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].task_type.name
        return context
