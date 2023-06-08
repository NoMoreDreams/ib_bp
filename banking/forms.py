from django import forms

from .models.transaction import Transaction


class SendMoneyForm(forms.ModelForm):
    amount = forms.FloatField(min_value=0.01)
    account_number = forms.CharField(label="Beneficiary", max_length=24)
    information = forms.CharField(
        label="Information for beneficiary",
        required=False,
        widget=forms.Textarea(attrs={"rows": "2"}),
    )

    class Meta:
        model = Transaction
        fields = [
            "amount",
            "account_number",
            "information",
            "variable_symbol",
            "specific_symbol",
            "constant_symbol",
        ]
        widgets = {"payer": forms.TextInput(attrs={"readonly": True})}
