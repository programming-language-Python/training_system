from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm, ClosedQuestionForm, ClosedQuestionAnswerOptionFormSet
from apps.testing.models import Testing, ClosedQuestion
from apps.testing.models.completed_testing import CompletedTesting
from apps.testing.types import TaskType
from mixins import URLMixin, ContextMixin


class TestingCreateView(AbstractTestingCreateView):
    form_class = TestingForm

    def form_valid(self, form) -> HttpResponse | HttpResponseRedirect:
        is_title_in_completed_testings = CompletedTesting.objects.filter(
            title=form.instance.title
        ).exists()
        if is_title_in_completed_testings:
            return self._add_error_title_exists(form)
        form.instance.user = self.request.user
        return super(TestingCreateView, self).form_valid(form)


# TODO Этот класс дублируется
class TestingListView(ContextMixin, LoginRequiredMixin, ListView):
    login_url = 'user:login'
    model = Testing
    template_name = 'testing_list.html'
    APP_NAME = APP_NAME

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_list_data(is_teacher=self.request.user.is_teacher)
        return context


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
            context |= self.get_testing_update_url_data() | self.get_testing_delete_url_data()
            tasks = [
                TaskType(name='Закрытый вопрос', url='task_closed_question_create'),
                TaskType(name='Открытый вопрос', url='task_open_question_create'),
                TaskType(name='Установление последовательности', url='task_sequencing_create'),
                TaskType(name='Установление соответствия', url='task_establishing_accordance_create'),
            ]
            context['task_data'] = {}
            for task in tasks:
                context['task_data'][task.name] = f'{APP_NAME}:{task.url}'
        return context


class TestingUpdateView(LoginRequiredMixin, UpdateView):
    model = Testing
    form_class = TestingForm
    template_name = 'testing_update.html'


class TestingDeleteView(DeleteView):
    model = Testing
    success_url = reverse_lazy(APP_NAME + ':testing_list')
    template_name = 'testing_confirm_delete.html'


class ClosedQuestionCreateView(CreateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    template_name = 'testing/task/closed_question_create_or_update.html'
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        testing_pk = self.kwargs['testing_pk']
        quantity_tasks = Testing.objects.get(pk=testing_pk).testing_related.count()
        context_form_fields = context['form'].fields
        context_form_fields['serial_number'].initial = quantity_tasks + 1
        context_form_fields['testing'].initial = testing_pk
        context['answer_option_form_set'] = ClosedQuestionAnswerOptionFormSet()
        for form in context['answer_option_form_set'].forms:
            form.fields['closed_question'].widget.attrs = {'data-name': 'closed-question'}
            form.fields['DELETE'].widget.attrs = {'data-name': 'delete'}
        context['btn_text'] = 'Создать задачу'
        return context

    def post(self, request, *args, **kwargs):
        closed_question_form = self.form_class(request.POST)
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(request.POST, request.FILES)
        if closed_question_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(closed_question_form, answer_option_form_set)
        else:
            return self.form_invalid(closed_question_form, answer_option_form_set)

    def form_valid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        closed_question = closed_question_form.save()
        answer_option_form_set.instance = closed_question
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:testing_detail', pk=self.kwargs['testing_pk'])

    def form_invalid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=closed_question_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )


class ClosedQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    template_name = 'testing/task/closed_question_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(instance=self.get_object())
        answer_option_form_set.extra = 0
        context['answer_option_form_set'] = answer_option_form_set
        for form in context['answer_option_form_set'].forms:
            form.fields['closed_question'].widget.attrs = {'data-name': 'closed-question'}
            form.fields['DELETE'].widget.attrs = {'data-name': 'delete'}
        context['btn_text'] = 'Обновить задачу'
        return context

    def post(self, request, *args, **kwargs):
        closed_question_form = self.form_class(request.POST, instance=self.get_object())
        answer_option_form_set = ClosedQuestionAnswerOptionFormSet(
            request.POST,
            request.FILES,
            instance=self.get_object()
        )
        if closed_question_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(closed_question_form, answer_option_form_set)
        else:
            return self.form_invalid(closed_question_form, answer_option_form_set)

    def form_valid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        closed_question_form.save()
        answer_option_form_set.save()
        return redirect(f'{APP_NAME}:task_closed_question_update', pk=self.kwargs['pk'])

    def form_invalid(
            self,
            closed_question_form: ClosedQuestionForm,
            answer_option_form_set: ClosedQuestionAnswerOptionFormSet
    ):
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=closed_question_form,
                answer_option_form_set=answer_option_form_set,
                # answer_option_form_set_errors=answer_option_form_set.errors
            )
        )


class ClosedQuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = ClosedQuestion

    def get_success_url(self):
        return reverse_lazy(f'{APP_NAME}:testing_detail', kwargs={'pk': self.request.GET['testing_pk']})


class OpenQuestionCreateView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError


class SequencingCreateView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError


class EstablishingAccordanceCreateView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError
