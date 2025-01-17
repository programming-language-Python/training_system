from typing import MutableMapping

from django.views.generic import DetailView

from apps.testing.abstractions.abstract_views import AbstractTaskView


class AbstractTaskDetailView(AbstractTaskView, DetailView):
    context_object_name = 'task'
    template_name: str

    def get_context_data(self, **kwargs) -> MutableMapping:
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.type
        return context
