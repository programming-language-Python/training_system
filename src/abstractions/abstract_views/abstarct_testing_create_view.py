from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView


class AbstractTestingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'testing_create.html'

    def _add_error_title_exists(self, form) -> HttpResponse:
        form.add_error('title', 'Тестирование с таким Наименование уже существует.')
        context = {
            'form': form
        }
        return render(self.request, 'testing_create.html', context)
