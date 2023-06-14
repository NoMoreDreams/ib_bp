from django.urls import path

from . import views
from .views import CustomLoginView, CustomLogoutView
urlpatterns = [
    # path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("login/verification/", views.email_verification, name="verification"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.ActivateView.as_view(), name='activate'),
    path('email_sent/', views.EmailSentView.as_view(), name='email_sent'),
]
