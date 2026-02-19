from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from common.forms import LessonForm
from common.models import Lesson, StudentClass, LessonVisits, Grades


def teacher_page(request):
    return 'Ok teacher page'

@method_decorator(login_required, name='dispatch')
class TeacherLessonsView(View):
    template_name = 'teacher_lessons.html'
    form_class = LessonForm

    def get(self, request):
        create_lesson_form = self.form_class()
        teacher_lessons_data = Lesson.objects.filter(teacher=request.user).all()
        return render(request, self.template_name,
                      context={'form': create_lesson_form, 'teacher_lessons': teacher_lessons_data})

    def post(self, request):
        create_lesson_form = self.form_class(request.POST)
        if create_lesson_form.is_valid():
            lesson = Lesson(teacher=request.user, **create_lesson_form.cleaned_data)
            lesson.save()
            return redirect('teacher_lessons')
        teacher_lessons_data = Lesson.objects.filter(teacher=request.user).all()
        return render(request, self.template_name,
                      context={'form': create_lesson_form, 'teacher_lessons': teacher_lessons_data})

@method_decorator(login_required, name='dispatch')
class TeacherSpecificLessonView(View):
    template_name = 'teacher_specific_lesson.html'

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        current_class = lesson.school_class
        student_in_class = [itm.student for itm in StudentClass.objects.filter(school_class=current_class).all()]

        absence_students_ids = [itm.student.id for itm in
                                LessonVisits.objects.filter(lesson=lesson).all()]  # write students who are absent

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
        return redirect('teacher_specific_lesson', lesson_id=lesson_id)


class AbsenceView(View):
    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)

        submitted_ids = [int(v) for k, v in request.POST.items() if k.startswith('student')]

        class_students = [itm.student for itm in
                          StudentClass.objects.filter(school_class=lesson.school_class).all()]

        for student in class_students:
            exists = LessonVisits.objects.filter(lesson=lesson, student=student).exists()
            if student.id in submitted_ids and not exists:
                LessonVisits.objects.create(lesson=lesson, student=student)
            elif student.id not in submitted_ids and exists:
                LessonVisits.objects.filter(lesson=lesson, student=student).delete()

        return redirect('teacher_specific_lesson', lesson_id=lesson_id)

class GradeView(View):
    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        current_class = lesson.school_class
        student_in_class = [itm.student for itm in StudentClass.objects.filter(school_class=current_class).all()]

        for student in student_in_class:
            grade = Grades.objects.filter(lesson=lesson, student=student).first()
            student.grade = grade.grade if grade else ""

        form = LessonForm(instance=lesson)
        return render(request, 'teacher_specific_lesson.html',
                      context={'form': form, 'lessons': lesson, 'class_students': student_in_class})

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        teacher = request.user

        for key, value in request.POST.items():
            if key.startswith('grade_'):
                student_id = int(key.replace('grade_', ''))

                if value.strip() == '':
                    continue

                try:
                    grade_value = int(value)
                except ValueError:
                    continue

                Grades.objects.update_or_create(
                    student_id=student_id,
                    lesson=lesson,
                    teacher=teacher,
                    defaults={'grade': grade_value}
                )

        return redirect('teacher_specific_lesson', lesson_id=lesson_id)

def check_student_homework(request, lesson_id, homework_id):
    return f'Ok check homework id {homework_id} for lesson id {lesson_id}'
