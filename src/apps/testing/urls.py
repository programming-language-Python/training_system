from django.urls import path

from .constants import APP_NAME
from .views.task_views import TaskDeleteView
from .views.task_views.closed_question_views import ClosedQuestionCreateView, ClosedQuestionUpdateView, \
    ClosedQuestionDetailView
from .views.task_views.open_question_views import OpenQuestionCreateView, OpenQuestionUpdateView, OpenQuestionDetailView
from .views.task_views.sequencing_views import SequencingCreateView, SequencingUpdateView
from .views.testing_views import TestingCreateView, TestingUpdateView, TestingDeleteView
from .views.testing_views.testing_detail_view import show_testing_detail_view

app_name = APP_NAME
urlpatterns = [
    path('journal/<journal_pk>/create/', TestingCreateView.as_view(), name='testing_create'),

    path('detail/<pk>', show_testing_detail_view, name='testing_detail'),
    path('update/<pk>', TestingUpdateView.as_view(), name='testing_update'),
    path('delete/<pk>', TestingDeleteView.as_view(), name='testing_delete'),

    path('<testing_pk>/task/closed_question/<type>/create', ClosedQuestionCreateView.as_view(),
         name='task_closed_question_create'),
    path('task/closed_question/detail/<pk>', ClosedQuestionDetailView.as_view(),
         name='task_closed_question_detail'),
    path('task/closed_question/update/<pk>', ClosedQuestionUpdateView.as_view(),
         name='task_closed_question_update'),

    path('<testing_pk>/task/open_question/<type>/create', OpenQuestionCreateView.as_view(),
         name='task_open_question_create'),
    path('task/open_question/detail/<pk>', OpenQuestionDetailView.as_view(),
         name='task_open_question_detail'),
    path('task/open_question/update/<pk>', OpenQuestionUpdateView.as_view(),
         name='task_open_question_update'),

    path('<testing_pk>/task/sequencing/<type>/create', SequencingCreateView.as_view(),
         name='task_sequencing_create'),
    path('task/sequencing/update/<pk>', SequencingUpdateView.as_view(),
         name='task_sequencing_update'),

    path('task/delete/<pk>', TaskDeleteView.as_view(), name='task_delete'),
]
