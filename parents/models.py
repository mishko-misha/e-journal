from django.db import models

class Parent(models.Model):
    parent=models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name='student')
    student=models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name='parents')