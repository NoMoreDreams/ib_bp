from django.db import models


class Account(models.Model):
    iban = models.CharField(max_length=24)
    balance = models.FloatField(default=100_000)
