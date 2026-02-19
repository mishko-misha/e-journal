from django.test import TestCase, Client
from django.urls import reverse

from common.models import Lesson, SchoolClass, LessonVisits, StudentClass


class TeacherTests(TestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="jhock", password="123456")


    def test_teacher_page(self):
        response = self.client.get('/teacher/lessons/')
        self.assertEqual(response.status_code, 200)

    def test_teacher_lessons_create(self):
        response = self.client.post('/teacher/lessons/',
                                    {"subject": 1, "lesson_date": "2026-01-31", "lesson_name": "Mathematics",
                                     "description": "Algebra", "home_work": "Solve equations", "school_class": 2})
        self.assertEqual(response.status_code, 302)
        created_lesson = Lesson.objects.get(lesson_name="Mathematics")
        self.assertIsNotNone(created_lesson)
        self.assertEqual(created_lesson.description, "Algebra")
        self.assertEqual(created_lesson.home_work, "Solve equations")
        self.assertEqual(created_lesson.school_class.pk, 2)

    def test_teacher_specific_lessons(self):
        response = self.client.post('/teacher/lessons/2')
        self.assertEqual(response.status_code, 301)

    def test_teacher_lessons_update(self):
        response = self.client.post('/teacher/lessons/14/',
                                    {"subject": 1, "lesson_date": "2026-01-28", "lesson_name": "Music",
                                     "description": "Learn new heavy metal", "home_work": "play to guitar", "school_class": 2})
        self.assertEqual(response.status_code, 302)
        updated_lesson = Lesson.objects.get(pk=14)
        self.assertEqual(updated_lesson.lesson_name, "Music")

    def test_set_absence(self):
        current_lesson = Lesson.objects.get(pk=14)
        school_class = current_lesson.school_class
        # Get all students
        student_in_class = StudentClass.objects.filter(school_class=school_class).select_related('student')

        students = [itm.student for itm in student_in_class]

        self.assertEqual(len(students), 3)

        # Set absence for one student
        post_data = {f"student-{students[0].id}": str(students[0].id)}

        response = self.client.post(f'/teacher/lessons/{current_lesson.id}/absence/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LessonVisits.objects.filter(lesson=current_lesson,student=students[0]).exists())

        # Set absence for two students
        post_data = {f"student-{students[1].id}": str(students[1].id),
                     f"student-{students[2].id}": str(students[2].id)}
        response = self.client.post(f'/teacher/lessons/{current_lesson.id}/absence/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LessonVisits.objects.filter(lesson=current_lesson, student=students[1]).exists())
        self.assertTrue(LessonVisits.objects.filter(lesson=current_lesson, student=students[2]).exists())