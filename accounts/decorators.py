from django.http import HttpResponseForbidden
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator


def manufacturer_required(view_func):
    return role_required('manufacturer')(view_func)

def consumer_required(view_func):
    return role_required('consumer')(view_func)

def pharmacy_required(view_func):
    return role_required('pharmacist')(view_func)

def distributor_required(view_func):
    return role_required('distributor')(view_func)


