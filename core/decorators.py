from django.shortcuts import redirect
from django.urls import reverse


def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return redirect(reverse('core:index'))
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
