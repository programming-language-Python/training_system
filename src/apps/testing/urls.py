from django.urls import path

from .constants import APP_NAME
from .views.task_views.closed_question_views import ClosedQuestionCreateView, ClosedQuestionUpdateView, \
    ClosedQuestionDeleteView
from .views.task_views.establishing_accordance_views import EstablishingAccordanceCreateView
from .views.task_views.open_question_views import OpenQuestionCreateView, OpenQuestionUpdateView, OpenQuestionDeleteView
from .views.task_views.sequencing_views import SequencingCreateView
from .views.testing_views import TestingCreateView, TestingListView, TestingDetailView, TestingUpdateView, \
    TestingDeleteView

app_name = APP_NAME
urlpatterns = [
    path('create/', TestingCreateView.as_view(), name='testing_create'),
    path('testing_list/', TestingListView.as_view(), name='testing_list'),
    path('detail/<pk>', TestingDetailView.as_view(), name='testing_detail'),
    path('update/<pk>', TestingUpdateView.as_view(), name='testing_update'),
    path('delete/<pk>', TestingDeleteView.as_view(), name='testing_delete'),

    path('<testing_pk>/task/create/closed_question', ClosedQuestionCreateView.as_view(),
         name='task_closed_question_create'),
    path('task/closed_question/update/<pk>', ClosedQuestionUpdateView.as_view(),
         name='task_closed_question_update'),
    path('task/closed_question/delete/<pk>', ClosedQuestionDeleteView.as_view(),
         name='task_closed_question_delete'),

    path('<testing_pk>/task/open_question/create', OpenQuestionCreateView.as_view(), name='task_open_question_create'),
    path('task/open_question/update/<pk>', OpenQuestionUpdateView.as_view(),
         name='task_open_question_update'),
    path('task/open_question/delete/<pk>', OpenQuestionDeleteView.as_view(),
         name='task_open_question_delete'),

    path('<testing_pk>/task/sequencing/create', SequencingCreateView.as_view(), name='task_sequencing_create'),
    path('<testing_pk>/task/establishing_accordance/create', EstablishingAccordanceCreateView.as_view(),
         name='task_establishing_accordance_create'),
]
