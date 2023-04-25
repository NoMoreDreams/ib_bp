from django.urls import path

from . import views
from .views import UserLoginView

urlpatterns = [
    # path('login/', views.login, name="login_page"),
    path('login/', UserLoginView.as_view(), name="login_page"),
    path('login/verification/', views.email_verification, name="verification"),
]
