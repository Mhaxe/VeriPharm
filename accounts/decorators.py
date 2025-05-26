from functools import wraps
from django.shortcuts import redirect

def manufacturer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'manufacturer':
            return view_func(request, *args, **kwargs)
        return redirect('login')  # or a 403 page if you'd prefer
    return _wrapped_view
