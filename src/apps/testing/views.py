from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from abstractions.abstract_views import AbstractTestingCreateView
from apps.testing.constants import APP_NAME
from apps.testing.forms import TestingForm, ClosedQuestionForm, AnswerOptionFormSet
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


class ClosedQuestionCreatedView(CreateView):
    model = ClosedQuestion
    form_class = ClosedQuestionForm
    template_name = 'testing/task/closed_question_create.html'
    pk_url_kwarg = 'testing_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_option_form_set'] = AnswerOptionFormSet()
        return context

    def post(self, request, *args, **kwargs):
        closed_question_form = self.form_class(request.POST)
        answer_option_form_set = AnswerOptionFormSet(request.POST, request.FILES)
        if closed_question_form.is_valid() and answer_option_form_set.is_valid():
            return self.form_valid(closed_question_form, answer_option_form_set)
        else:
            return self.form_invalid(closed_question_form, answer_option_form_set)

    def form_valid(self, closed_question_form: ClosedQuestionForm, answer_option_form_set: AnswerOptionFormSet):
        new_closed_question = closed_question_form.save(commit=False)
        new_closed_question.testing_id = self.kwargs['testing_pk']
        new_closed_question.save()
        for answer_option_form in answer_option_form_set:
            answer_option = answer_option_form.save(commit=False)
            photo = answer_option.photo
            if not photo.closed:
                file_system = FileSystemStorage()
                file_system.save(photo.name, photo.file)
            answer_option.closed_question_id = new_closed_question.pk
            answer_option.save()
        # raise NotImplementedError('Сделать redirect')
        return redirect('testing_by_code:task_detail', pk=task_service.get_pk())

    def form_invalid(self, closed_question_form: ClosedQuestionForm, answer_option_form_set: AnswerOptionFormSet):
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                closed_question_form=closed_question_form,
                answer_option_form=answer_option_form_set
            )
        )


class OpenQuestionCreatedView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError


class SequencingCreatedView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError


class EstablishingAccordanceCreatedView(CreateView):
    pk_url_kwarg = 'testing_pk'

    def __init__(self):
        raise NotImplementedError
