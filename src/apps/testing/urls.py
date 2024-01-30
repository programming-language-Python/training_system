from django.urls import path

from .views import *

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
    path('<testing_pk>/task/sequencing/create', SequencingCreateView.as_view(), name='task_sequencing_create'),
    path('<testing_pk>/task/establishing_accordance/create', EstablishingAccordanceCreateView.as_view(),
         name='task_establishing_accordance_create'),
]
