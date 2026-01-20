from django.shortcuts import render

# Create your views here.

def parents_page(request):
    return 'ok'

def parents_student(request,student_id):
    return f'ok {student_id}'

def student_lesson_for_parents(request,lesson_id):
    return f'ok {lesson_id}'
