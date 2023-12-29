from django.urls import path

from .views import *

app_name = 'testing'
urlpatterns = [
    path('create/', TestingCreateView.as_view(), name='testing_create'),
    path('testing_list/', TestingListView.as_view(), name='testing_list'),
    path('<pk>/detail/', TestingDetailView.as_view(), name='testing_detail'),
]
