from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    iban = models.CharField(max_length=24)
    balance = models.FloatField(default=100_000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
