from django.shortcuts import render


def login(request):
    return render(request, "login/login_page.html", {})


def email_verification(request):
    return render(request, "login/verification.html", {})
