from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from banking.forms import SendMoneyForm
from banking.models.account import Account
from banking.models.transaction import Transaction


class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = "accounts"
    template_name = "banking/account_list.html"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountsDetailView(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = "account"
    template_name = "banking/account_detail.html"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the transaction filter parameters from the URL query string
        from_date_str = self.request.GET.get("date_from")
        to_date_str = self.request.GET.get("date_to")
        beneficiary = self.request.GET.get("beneficiary")

        # Convert the date strings to datetime objects
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else None
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') if to_date_str else None

        # Filter the transactions based on the parameters
        transactions = Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by(
            "-created")
        if from_date:
            transactions = transactions.filter(created__gte=from_date)
        if to_date:
            transactions = transactions.filter(created__lte=to_date)
        if beneficiary:
            transactions = transactions.filter(beneficiary_id=beneficiary)

        context["transactions"] = transactions
        context["accounts"] = {transaction.beneficiary for transaction in Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by(
            "-created")}
        context["from_date"] = from_date_str
        context["to_date"] = to_date_str
        if beneficiary:
            context["selected_beneficiary"] = int(beneficiary)
        else:
            context["selected_beneficiary"] = beneficiary

        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "banking/transaction_form.html"
    form_class = SendMoneyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payer_account = get_object_or_404(Account, user=self.request.user, pk=self.kwargs["pk"])
        context["payer_account"] = payer_account
        return context

    def form_valid(self, form):
        payer_account = get_object_or_404(Account, user=self.request.user, pk=self.kwargs["pk"])
        account_number = form.cleaned_data["account_number"]
        try:
            beneficiary_account = Account.objects.get(number=account_number)
        except Account.DoesNotExist:
            form.add_error("account_number", "Please enter correct beneficiary account number")
            return super().form_invalid(form)

        if beneficiary_account == payer_account:
            form.add_error("account_number", "Payer account cannot be the same as the beneficiary's account")
            return super().form_invalid(form)

        amount = form.cleaned_data["amount"]
        if amount > payer_account.balance:
            form.add_error("amount", "Transaction amount cannot be greater than the payer\'s account balance")
            return self.form_invalid(form)

        # Subtract the amount from the payer's balance and save the account
        payer_account.balance -= amount
        payer_account.save()

        # Add the amount to the beneficiary's balance and save the account
        beneficiary_account.balance += amount
        beneficiary_account.save()

        # Set the current user as the payer and save the transaction
        transaction = form.save(commit=False)
        transaction.payer = payer_account
        transaction.beneficiary = beneficiary_account
        transaction.account = payer_account
        transaction.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"pk": self.kwargs["pk"]})
