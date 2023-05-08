from django.db import models

from banking.models.account import Account


class Transaction(models.Model):
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    payer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payer_transaction_set')
    beneficiary = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='beneficiary_transaction_set')
    information = models.TextField(null=True, blank=True)
    variable_symbol = models.CharField(null=True, blank=True, max_length=100)
    specific_symbol = models.CharField(null=True, blank=True, max_length=100)
    constant_symbol = models.CharField(null=True, blank=True, max_length=100)
