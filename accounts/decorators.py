from functools import wraps
from django.shortcuts import redirect

def manufacturer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'manufacturer':
            return view_func(request, *args, **kwargs)
        return redirect('login')  
    return _wrapped_view

def distro_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'distributer':
            return view_func(request, *args, **kwargs)
        return redirect('login')  
    return _wrapped_view