from django.shortcuts import render

# Create your views here.
def login(request):
    return 'ok'

def register(request):
    return 'ok'

def logout(request):
    return 'ok'

def user_view(request, user_id):
    return f'ok {user_id}'