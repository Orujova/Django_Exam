from django.shortcuts import redirect




def check_user_login(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return func(request, *args, **kwargs)
    return wrapper