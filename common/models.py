from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)


class SchoolClass(models.Model):
    start_year = models.IntegerField()
    letter = models.CharField(max_length=1)


class StudentClass(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)


class Contacts(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)


class Lesson(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson_date = models.DateField()
    lesson_name = models.CharField(max_length=100)
    description = models.TextField()
    home_work = models.TextField()
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)


class Files(models.Model):
    file = models.FileField(upload_to='lesson_files/')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)


class Grades(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='grades_as_student')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='grades_as_teacher')


class StudentHomeWork(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    home_work = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    text_data = models.TextField()
    grade = models.ForeignKey('Grades', on_delete=models.CASCADE)


class LessonVisits(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
