from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("accounts/", views.AccountsListView.as_view(), name="account_list"),
    path("accounts/<int:pk>", views.AccountsDetailView.as_view(), name="account_detail"),
    path("accounts/<int:pk>/transactions/new", views.TransactionCreateView.as_view(), name="transaction_create"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
