from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    number = models.CharField(max_length=24)
    balance = models.FloatField(default=100_000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s account ({self.number})"

    @property
    def iban(self) -> str:
        country_code = 'SK'
        bank_code = '1100'
        account_prefix = '000000'

        iban = f"{bank_code}{account_prefix}{self.number}"
        check_digits = '{:02d}'.format(98 - (int(iban) * 100 % 97))

        iban = f"{country_code}{check_digits}{bank_code}{account_prefix}{self.number}"
        return iban
