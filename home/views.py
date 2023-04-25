from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, "home/home_page.html", {})

def accounts(request):
    return render(request, "home/accounts.html", {})


@login_required(login_url="/admin")
def authorized(request):
    return render(request, "home/authorized.html", {})
