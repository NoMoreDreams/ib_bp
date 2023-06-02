from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from custom_auth.forms import RegisterForm


class CustomRegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "custom_auth/register_page.html"


class CustomLoginView(LoginView):
    template_name = "custom_auth/login_page.html"
    success_url = reverse_lazy("account_list")
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    template_name = "custom_auth/logout_page.html"
    success_url = reverse_lazy("login")


def email_verification(request):
    return render(request, "custom_auth/verification.html", {})
