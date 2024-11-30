from django.http import HttpResponseForbidden
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
