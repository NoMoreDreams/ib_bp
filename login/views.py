from django.shortcuts import render
from django.contrib.auth.views import LoginView


# def login(request):
#     return render(request, "login/login_page.html", {})

class UserLoginView(LoginView):
    template_name = "login/login_page.html"


def email_verification(request):
    return render(request, "login/verification.html", {})
