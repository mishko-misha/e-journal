from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from common.forms import LessonForm
from common.models import Lesson, StudentClass, LessonVisits


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
    return render(request, 'teacher_lessons.html',
                  context={'form': create_lesson_form, 'teacher_lessons': teacher_lessons_data})


class TeacherSpecificLessonView(View):
    template_name = 'teacher_specific_lesson.html'

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        current_class = lesson.school_class
        student_in_class = [itm.student for itm in StudentClass.objects.filter(school_class=current_class).all()]

        absence_students_ids = [itm.student.id for itm in LessonVisits.objects.filter(lesson=lesson).all()]

        for student in student_in_class:
            student.is_absent = "checked" if student.id in absence_students_ids else ""

        form = LessonForm(instance=lesson)
        return render(request, self.template_name,
                      context={'form': form, 'lessons': lesson, 'class_students': student_in_class})

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        form = LessonForm(request.POST, instance=lesson)
        form.is_valid()
        form.save()
        return redirect(self.template_name, lesson_id=lesson_id)


class AbsenceView(View):
    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)

        for key, value in request.POST.items():
            if key.startswith('student'):
                student = User.objects.get(id=value)
                lesson_absence_student_form = LessonVisits.objects.create(lesson=lesson, student=student)
                lesson_absence_student_form.save()
        return redirect('teacher_specific_lesson', lesson_id=lesson_id)


def grade(request, lesson_id):
    return f'Ok grade for lesson id {lesson_id}'


def check_student_homework(request, lesson_id, homework_id):
    return f'Ok check homework id {homework_id} for lesson id {lesson_id}'
