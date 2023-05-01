from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from banking.models.account import Account
from banking.models.transaction import Transaction


class AccountsListView(ListView):
    model = Account
    context_object_name = "accounts"
    template_name = "banking/account_list.html"


class AccountsDetailView(DetailView):
    model = Account
    context_object_name = "account"
    template_name = "banking/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(Q(payer=self.object) | Q(beneficiary=self.object))
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    fields = "__all__"
    template_name = "banking/transaction_form.html"

    def form_valid(self, form):
        form.instance.account = Account.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"pk": self.kwargs["pk"]})
