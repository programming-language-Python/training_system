from django.urls import path

from .views.solving_testing_views import StudentSolvingTestingDetailView
from .views.task_views import TaskDetailView, update_task, duplicate_task, delete_task, add_task_form
from .views.testing_views import TestingCreateView, TestingUpdateView, \
    TestingDeleteView, TeacherTestingDetailView
from .views.testing_views.testing_detail_view import redirect_testing_detail_view

app_name = 'testing_by_code'
urlpatterns = [
    path('journal/<journal_pk>/create/', TestingCreateView.as_view(), name='testing_create'),
    path('<pk>/redirect_detail', redirect_testing_detail_view, name='testing_detail'),
    path('<pk>/detail', TeacherTestingDetailView.as_view(), name='teacher_testing_detail'),
    path('<pk>/solving_task_list', StudentSolvingTestingDetailView.as_view(), name='student_testing_detail'),

    path('<pk>/update/', TestingUpdateView.as_view(), name='testing_update'),
    path('<pk>/delete/', TestingDeleteView.as_view(), name='testing_delete'),
    path('task/<pk>/detail/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<pk>/update/', update_task, name='update_task'),
    path('task/<pk>/duplicate/', duplicate_task, name='duplicate_task'),
    path('task/<pk>/delete/', delete_task, name='delete_task'),
    path('add_task_form/', add_task_form, name='add_task_form'),
]
