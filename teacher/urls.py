from django.urls import path

from . import views

urlpatterns = [
    path('', views.teacher_page, name='teacher_page'),
    path('lessons/', views.TeacherLessonsView.as_view(), name='teacher_lessons'),
    path('lessons/<lesson_id>/', views.TeacherSpecificLessonView.as_view(), name='teacher_specific_lesson'),
    path('lessons/<lesson_id>/absence/', views.AbsenceView.as_view(), name='absence'),
    path('lessons/<lesson_id>/grade/', views.GradeView.as_view(), name='grade'),
    path('lessons/<lesson_id>/homework/<homework_id>/', views.check_student_homework, name='check_student_homework'),
]
