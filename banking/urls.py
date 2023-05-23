from django.urls import path

from . import views
from .views import UpdateAccountNameView

urlpatterns = [
    path("accounts/", views.AccountsListView.as_view(), name="account_list"),
    path("accounts/<slug:slug>", views.AccountDetailView.as_view(), name="account_detail"),
    path("accounts/<slug:slug>/transactions/new/", views.TransactionCreateView.as_view(), name="transaction_create"),
    path("accounts/<slug:slug>/transactions", views.TransactionListView.as_view(), name="transaction_list"),
    path("", views.landing_page_view, name="landing_page"),
    path('account/<slug:slug>/update-name/', UpdateAccountNameView.as_view(), name='update_account_name'),
    path("accounts/<slug:slug>/transactions/<int:transaction_id>/duplicate/", views.DuplicateTransactionView.as_view(), name="duplicate_transaction"),

]
