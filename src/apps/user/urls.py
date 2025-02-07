from django.urls import path

from apps.user.constants import APP_NAME
from apps.user.views import LoginUser, CustomLogoutView, TestingListView, SolvingTestingListView
from apps.user.views.journal_views import TestingSettingJournalView, TestingResultJournalView, StudentJournalView
from apps.user.views.student_views import StudentTemplateView
from apps.user.views.teacher_views import TeacherTemplateView

app_name = APP_NAME

urlpatterns = [
    path('', LoginUser.as_view(), name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('student/', StudentTemplateView.as_view(), name='student_detail'),
    path('journal/student/', StudentJournalView.as_view(),
         name='student_journal'),

    path('teacher/', TeacherTemplateView.as_view(), name='teacher_detail'),

    path('journal/<journal_pk>/testing_list_view/', TestingListView.as_view(), name='testing_list'),
    path('journal/<journal_pk>/student/<student_pk>/solving_testing_list_view/', SolvingTestingListView.as_view(),
         name='solving_testing_list'),

    path('journal/testing_setting_journal/', TestingSettingJournalView.as_view(),
         name='testing_setting_journal'),
    path('journal/testing_result_journal/', TestingResultJournalView.as_view(),
         name='testing_result_journal'),
]
