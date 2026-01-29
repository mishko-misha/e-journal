from django.shortcuts import render, redirect

from common.forms import LessonForm
from common.models import Lesson


def teacher_page(request):
    return 'Ok teacher page'


def teacher_lessons(request):
    if request.method == 'POST':
        create_lesson_form = LessonForm(request.POST)

        if create_lesson_form.is_valid():
            lesson = Lesson(teacher=request.user, **create_lesson_form.cleaned_data)
            lesson.save()
            return redirect('teacher_lessons')
    else:
        create_lesson_form = LessonForm()
    teacher_lessons_data = Lesson.objects.filter(teacher=request.user).all()
    return render(request, 'teacher_lessons.html',context={'form': create_lesson_form, 'teacher_lessons': teacher_lessons_data})


def teacher_specific_lesson(request, lesson_id):
    return f'Ok lesson id is {lesson_id}'


def absence(request, lesson_id):
    return f'Ok absence for lesson id {lesson_id}'


def grade(request, lesson_id):
    return f'Ok grade for lesson id {lesson_id}'


def check_student_homework(request, lesson_id, homework_id):
    return f'Ok check homework id {homework_id} for lesson id {lesson_id}'