from django.urls import path

from .views import *

app_name = 'testing'
urlpatterns = [
    path('testing/create/', TestingCreateView.as_view(), name='testing_create'),
    path('testing_list/', TestingListView.as_view(), name='testing_list'),
    path('testing/<pk>/detail/', TestingDetailView.as_view(), name='testing_detail'),
    path('testing/<pk>/update/', TestingUpdateView.as_view(), name='testing_update'),
    path('testing/<pk>/delete/', TestingDeleteView.as_view(), name='testing_delete'),
    path('task/<pk>/detail/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<pk>/update/', update_task, name='update_task'),
    path('task/<pk>/duplicate/', duplicate_task, name='duplicate_task'),
    path('task/<pk>/delete/', delete_task, name='delete_task'),
    path('add_task_form/', add_task_form, name='add_task_form'),
    path('completed_testing_create/', create_completed_testing, name='completed_testing_create'),
]
