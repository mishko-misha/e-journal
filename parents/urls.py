from django.urls import path

from . import views

urlpatterns = [
    path('',views.parents_page,name='parents_page'),
    path('student/<student_id>',views.parents_student,name='parents_student'),
    path('lessons/<lesson_id>',views.student_lesson_for_parents,name='student_lesson_for_parents'),
]