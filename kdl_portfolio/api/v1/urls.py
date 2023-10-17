"""
URLs for edx_careerpaths.
"""
from django.urls import path, re_path  # pylint: disable=unused-import
from . import views

app_name = 'v1'
urlpatterns = [
    path('profiles/<str:username>', views.get_student_profile, name='Student'),
    path('student_career_info/', views.StudentCareerInfoAPIView.as_view(), name='Student Career Info'),
    path('student_career_info/<str:username>', views.StudentCareerInfoAPIView.as_view(), name='Student Career Info'),
    path('projects/', views.ProjectAPIView.as_view(), name="Projects"),
    path('projects/<str:username>', views.get_student_projects, name="Student Projects")
    # path('student/', views.get_student_info, name="Student Information")
]