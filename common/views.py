from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from common.forms import *

class LoginView(View):
    form = LoginForm
    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name, context={'form': self.form()})

    def post(self, request):
        user_login = self.form(request.POST)
        user_login.is_valid()
        user = auth.authenticate(request, username=user_login.cleaned_data['login'],
                                 password=user_login.cleaned_data['password'])
        if user is not None:
            auth.login(request, user)
            return redirect("/user/" + str(user.id) + "/")
        else:
            return render(request, self.template_name, {'error': 'Invalid login or password'})

class RegisterView(View):
    form = RegisterForm
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, self.template_name, context={'form': form})

class LogoutView(View):
    def get(self, request):
        return redirect("login")

    def post(self, request):
        auth.logout(request)
        return redirect("login")

class UserView(LoginRequiredMixin, View):
    template_name = 'user_page.html'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_group = user.groups.all()[0]
        return render(request, self.template_name, {'user': user, 'user_group': user_group.name})