from django.shortcuts import render

# Create your views here.
def teacher_page(request):
    return 'Ok teacher page'


def teacher_lessons(request):
    return 'Ok lessons page'


def specific_lesson(request, lesson_id):
    return f'Ok lesson id is {lesson_id}'


def absence(request, lesson_id):
    return f'Ok absence for lesson id {lesson_id}'


def grade(request, lesson_id):
    return f'Ok grade for lesson id {lesson_id}'


def check_student_homework(request, lesson_id, homework_id):
    return f'Ok check homework id {homework_id} for lesson id {lesson_id}'