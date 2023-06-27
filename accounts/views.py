from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from .forms import LoginForm, RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.conf import settings
from .decorators import check_user_login


User = get_user_model()


@check_user_login
def login_view(request):
    form = LoginForm()
    print("GET request: ", request.GET)
    next = request.GET.get("next")

    if request.method == "POST":
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = User.objects.get(username=username)

            login(request, user)


            if next:
                return redirect(next)
            return redirect("Blog:home")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)



def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()

            
            token = PasswordResetTokenGenerator().make_token(user)
            uuid64 = urlsafe_base64_encode(smart_bytes(user.id))
            link = f"http://localhost:8000/accounts/activation/{uuid64}/{token}/"

           
            send_mail(
                "Activation",
                f"Please click the link below\n{link}",  
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            return redirect("Blog:home")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)



def logout_view(request):
    logout(request)
    return redirect("/")



def activation_view(request, uuid64, token):
    id = smart_str(urlsafe_base64_decode(uuid64))
    user = User.objects.get(id=id)

    if not PasswordResetTokenGenerator().check_token(user, token):
        message = "Link Duzgun Deyil"
        messages.error(request, message)
        return redirect("accounts:login")

    user.is_active = True
    user.save()

    login(request, user)
    return redirect("Blog:home")
