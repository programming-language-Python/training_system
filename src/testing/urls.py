from django.urls import path

from .views import *

app_name = 'testing'
urlpatterns = [
    path('testing/create/', TestingCreateView.as_view(), name='testing_create'),
    path('testing_list/', TestingListView.as_view(), name='testing_list'),
    path('testing/<pk>/detail/', TestingDetailView.as_view(), name='testing_detail'),
    path('testing/<pk>/update/', TestingUpdateView.as_view(), name='testing_update'),
    # path('testing/<pk>/delete/', TestingDeleteView.as_view(), name='testing_delete'),
    # path('testing/<pk>/delete/', testing_delete, name='testing_delete'),
    path('testing/<pk>/delete/', TestingDeleteView.as_view(), name='testing_delete'),
    # path('update_testing/<int:pk>/', UpdateTesting.as_view(), name='update_testing'),
    # path('testing/create/', create_testing, name='create_testing'),
    # path('task/<pk>/create/', create_task, name='create_task'),
    # path('task/<pk>/detail/', task_detail, name='task_detail'),

    # path('task/create/', TaskCreate.as_view(), name='task_create'),
    # path('task/<testing_pk>/create/', task_create, name='task_create'),
    path('task/<pk>/detail/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<pk>/update/', task_update, name='task_update'),
    path('task/<pk>/delete/', task_delete, name='task_delete'),
    path('add_task_form/', add_task_form, name='add_task_form'),

    path('serializer_of_test_answers/', serializer_of_test_answers, name='serializer_of_test_answers'),
]
