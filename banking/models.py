from django.db import models


class Transaction(models.Model):
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
