from django.urls import path

from .views import *

app_name = 'testing'
urlpatterns = [
    path('testing_by_code/create/', TestingCreateView.as_view(), name='testing_create'),
]
