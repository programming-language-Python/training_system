from django.urls import path

from apps.user.constants import APP_NAME
from apps.user.views import LoginUser, CustomLogoutView, TestingListView
from apps.user.views.student_views import StudentDetailView, StudentSolvingTestingListView, \
    StudentSolvingTestingByCodeListView
from apps.user.views.teacher_views import TeacherTemplateView

app_name = APP_NAME

urlpatterns = [
    path('', LoginUser.as_view(), name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('student/<pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student_solving_testing_list/<pk>/', StudentSolvingTestingListView.as_view(),
         name='student_solving_testing_list'),
    path('student_solving_testing_by_code_list/<pk>/', StudentSolvingTestingByCodeListView.as_view(),
         name='student_solving_testing_by_code_list'),

    path('teacher/', TeacherTemplateView.as_view(), name='teacher'),

    path('journal/<journal_pk>/testing_list_view/', TestingListView.as_view(), name='testing_list'),
]
