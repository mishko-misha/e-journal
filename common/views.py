from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from common.forms import *


def login(request):
    if request.method == 'POST':
        user_login = LoginForm(request.POST)
        user_login.is_valid()
        user = auth.authenticate(request, username=user_login.cleaned_data['login'],
                                 password=user_login.cleaned_data['password'])
        if user is not None:
            auth.login(request, user)
            return redirect("/user/" + str(user.id) + "/")
        else:
            return render(request, 'login.html', {'error': 'Invalid login or password'})
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        user = RegisterForm(request.POST)
        user.is_valid()
        user.save()
        return redirect("login")
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, "register.html", context)


def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url='login')
def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    user_group = user.groups.all()[0]
    return render(request, 'user_page.html', {'user': user, 'user_group': user_group.name})
