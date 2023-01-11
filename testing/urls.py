from django.urls import path

from .views import *

app_name = 'testing'

urlpatterns = [
    path('testing_list/', TestingList.as_view(), name='testing_list'),
    path('testing_update/<int:pk>/', UpdateTesting.as_view(), name='testing_update'),
    path('add_testing/', add_testing, name='add_testing'),
    path('create_task_setting_form/<int:number_of_forms>', create_task_setting_form, name='create_task_setting_form'),
]
