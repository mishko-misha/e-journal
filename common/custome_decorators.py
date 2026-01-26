from functools import wraps

from django.http import HttpResponseForbidden


def group_student_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Student').exists():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


def group_teacher_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Teacher').exists():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


def group_parent_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Parent').exists():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


def user_should_be(group_name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")

        return wrapper

    return decorator
