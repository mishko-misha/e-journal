from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form, CharField, DateInput, PasswordInput, forms

from common.models import Lesson


class RegisterForm(UserCreationForm):
    password1 = CharField(label='Password', widget=PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = CharField(label='Confirm Password', widget=PasswordInput(attrs={'autocomplete': 'new-password'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {
            'username': ''
        }

class LoginForm(Form):
    login = CharField(max_length=150)
    password = CharField(max_length=150, widget=PasswordInput)

class DateInputCustom(DateInput):
    input_type = 'date'

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ['teacher']
        widgets = {
            'lesson_date': DateInputCustom(attrs={'class': 'form-control'}),
        }