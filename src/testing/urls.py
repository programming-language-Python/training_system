from django.urls import path

from .views import *

app_name = 'testing'

urlpatterns = [
    path('testing_list/', TestingList.as_view(), name='testing_list'),
    # path('update_testing/<int:pk>/', UpdateTesting.as_view(), name='update_testing'),
    path('testing/create/', create_testing, name='create_testing'),
    path('testing/<pk>/update/', update_testing, name='update_testing'),
    path('task_setup/<id_of_one_test>/create/', create_task_setup, name='create_task_setup'),
    path('task_setup/<pk>/detail/', task_setup_detail, name='task_setup_detail'),
    path('task_setup/<pk>/update/', update_task_setup, name='update_task_setup'),
    path('task_setup/<pk>/delete/', delete_task_setup, name='delete_task_setup'),
    path('add_task_setup_form/', add_task_setup_form, name='add_task_setup_form'),
]
