from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from banking.forms import SendMoneyForm
from banking.models.account import Account
from banking.models.transaction import Transaction


class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = "accounts"
    template_name = "banking/account_list.html"
    extra_context = {"nvbar": "select_account"}

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = "account"
    template_name = "banking/account_detail.html"
    slug_field = "slug"
    extra_context = {"nbar": "home"}

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the transaction filter parameters from the URL query string
        # from_date_str = self.request.GET.get("date_from")
        # to_date_str = self.request.GET.get("date_to")
        # beneficiary = self.request.GET.get("beneficiary")
        #
        # # Convert the date strings to datetime objects
        # from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else None
        # to_date = datetime.strptime(to_date_str, '%Y-%m-%d') if to_date_str else None

        # Filter the transactions based on the parameters
        # transactions = Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by(
        #     "-created")
        # if from_date:
        #     transactions = transactions.filter(created__gte=from_date)
        # if to_date:
        #     transactions = transactions.filter(created__lte=to_date)
        # if beneficiary:
        #     transactions = transactions.filter(beneficiary_id=beneficiary)
        most_expensive_transaction = Transaction.objects.filter(payer=self.object).order_by("-amount").first()

        transaction_aggregate = Transaction.objects.filter(payer=self.object).values(
            'beneficiary__user__username').annotate(total_amount=Sum("amount"))
        beneficiaries = [item['beneficiary__user__username'] for item in transaction_aggregate]
        amounts = [item['total_amount'] for item in transaction_aggregate]
        context["beneficiaries"] = beneficiaries
        context["amounts"] = amounts
        context["most_expensive_transaction"] = most_expensive_transaction
        # context["accounts"] = {transaction.beneficiary for transaction in
        #                        Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by(
        #                            "-created")}
        # context["from_date"] = from_date_str
        # context["to_date"] = to_date_str
        # if beneficiary:
        #     context["selected_beneficiary"] = int(beneficiary)
        # else:
        #     context["selected_beneficiary"] = beneficiary

        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = "transactions"
    template_name = "banking/transaction_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "")
        current_acc = Account.objects.get(slug=self.kwargs["slug"])
        queryset = Transaction.objects.filter((Q(payer=current_acc) | Q(beneficiary=current_acc)) &
                                              (Q(amount__icontains=q) | Q(beneficiary__number__icontains=q)))

        return queryset.annotate(transaction_date=TruncDate("created")).order_by("-created")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = Account.objects.get(slug=self.kwargs["slug"])
        context["nbar"] = "transactions"

        transactions = context['transactions']

        grouped_transactions = {}
        for transaction in transactions:
            transaction_date = transaction.transaction_date.strftime('%d. %m. %Y')
            if transaction_date not in grouped_transactions:
                grouped_transactions[transaction_date] = []
            grouped_transactions[transaction_date].append(transaction)

        context['grouped_transactions'] = grouped_transactions
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # Get the transaction filter parameters from the URL query string
    #     from_date_str = self.request.GET.get("date_from")
    #     to_date_str = self.request.GET.get("date_to")
    #     beneficiary = self.request.GET.get("beneficiary")
    #
    #     # Convert the date strings to datetime objects
    #     from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else None
    #     to_date = datetime.strptime(to_date_str, '%Y-%m-%d') if to_date_str else None
    #
    #     # Filter the transactions based on the parameters
    #
    #     if from_date:
    #         transactions = transactions.filter(created__gte=from_date)
    #     if to_date:
    #         transactions = transactions.filter(created__lte=to_date)
    #     if beneficiary:
    #         transactions = transactions.filter(beneficiary_id=beneficiary)
    #
    #     context["transactions"] = transactions
    #     context["accounts"] = {transaction.beneficiary for transaction in Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object)).order_by(
    #         "-created")}
    #     context["from_date"] = from_date_str
    #     context["to_date"] = to_date_str
    #     if beneficiary:
    #         context["selected_beneficiary"] = int(beneficiary)
    #     else:
    #         context["selected_beneficiary"] = beneficiary
    #
    #     return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "banking/transaction_form.html"
    form_class = SendMoneyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payer_account = get_object_or_404(Account, user=self.request.user, slug=self.kwargs["slug"])
        context["payer_account"] = payer_account
        context["account"] = Account.objects.get(slug=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        payer_account = get_object_or_404(Account, user=self.request.user, slug=self.kwargs["slug"])
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

        if amount <= 0:
            form.add_error("amount", "Transaction amount must be greater than zero")
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
        return reverse_lazy("account_detail", kwargs={"slug": self.kwargs["slug"]})


def landing_page_view(request):
    return render(request, 'banking/landing_page.html')
