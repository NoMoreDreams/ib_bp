from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm

from banking.models.account import Account
from banking.models.transaction import Transaction


class CustomAccountChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"IBAN: {obj.iban}"


class CustomTransactionAdminForm(ModelForm):
    payer = CustomAccountChoiceField(queryset=Account.objects.all())
    beneficiary = CustomAccountChoiceField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = "__all__"


@admin.register(Transaction)
class BankingTransaction(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("amount", "date", "payer")
    list_display_links = ("amount",)
    list_filter = ("is_processed",)
    readonly_fields = ("date", "is_processed")
    form = CustomTransactionAdminForm


@admin.register(Account)
class BankingAccount(admin.ModelAdmin):
    list_display = ("number", "balance")
    list_filter = ("number",)
    list_display_links = ("number",)

    # @admin.display(description="IBAN", ordering="iban")
    # def format_iban(self, obj: Account):
    #     return obj.iban
