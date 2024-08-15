from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('', LoginUser.as_view(), name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('teacher/<pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('student/<pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student_solving_testing_list/<pk>/', StudentSolvingTestingListView.as_view(),
         name='student_solving_testing_list'),
    path('student_solving_testing_by_code_list/<pk>/', StudentSolvingTestingByCodeListView.as_view(),
         name='student_solving_testing_by_code_list'),
]
