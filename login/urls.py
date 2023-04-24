from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('login/verification/', views.email_verification),
]
