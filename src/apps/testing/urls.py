from django.urls import path

from .views import *

app_name = APP_NAME
urlpatterns = [
    path('create/', TestingCreateView.as_view(), name='testing_create'),
    path('testing_list/', TestingListView.as_view(), name='testing_list'),
    path('<pk>/detail/', TestingDetailView.as_view(), name='testing_detail'),
    path('<pk>/update/', TestingUpdateView.as_view(), name='testing_update'),
    path('<pk>/delete/', TestingDeleteView.as_view(), name='testing_delete'),
    path('<testing_pk>/create/task/closed_question', ClosedQuestionCreatedView.as_view(),
         name='task_closed_question_create'),
    path('<testing_pk>/create/task/open_question', OpenQuestionCreatedView.as_view(), name='task_open_question_create'),
    path('<testing_pk>/create/task/sequencing', SequencingCreatedView.as_view(), name='task_sequencing_create'),
    path('<testing_pk>/create/task/establishing_accordance', EstablishingAccordanceCreatedView.as_view(),
         name='task_establishing_accordance_create'),
]
