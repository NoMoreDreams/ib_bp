from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name="login_page"),
    path('login/verification/', views.email_verification, name="verification"),
]
