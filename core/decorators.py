from django.shortcuts import render


def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                error = f"You need to be in \"{group_name}\" group to acces this page."
                return render(request, "core/index.html", {
                    "error": error,
                })
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
