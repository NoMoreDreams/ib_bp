from django.urls import path

from . import views
from .views import CustomLoginView, CustomLogoutView, CustomRegisterView

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("login/verification/", views.email_verification, name="verification"),
]
