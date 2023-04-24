from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, "home/home_page.html", {})


@login_required(login_url="/admin")
def authorized(request):
    return render(request, "home/authorized.html", {})
