from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="home_page"),
    path('accounts/', views.accounts, name="accounts"),
    path('authorized/', views.authorized),
]
