from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by("-date")
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['amount', 'payer', 'beneficiary', 'information', 'variable_symbol', 'specific_symbol', 'constant_symbol']
    template_name = "banking/transaction_form.html"

    def form_valid(self, form):
        try:
            payer_account = form.cleaned_data["payer"]
            beneficiary_account = form.cleaned_data["beneficiary"]
            amount = form.cleaned_data["amount"]
        except KeyError:
            form.add_error("values", "Please enter correct payer account and amount to pay")
            return super().form_invalid(form)

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
        transaction.save()

        form.instance.account = Account.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"pk": self.kwargs["pk"]})
