from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Account(models.Model):
    number = models.CharField(max_length=24)
    balance = models.FloatField(default=100_000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"Používateľ {self.user} - účet ({self.number})"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.number)
        return super().save(*args, **kwargs)

    @property
    def iban(self) -> str:
        country_code = 'SK'
        bank_code = '1100'
        account_prefix = '000000'

        iban = f"{bank_code}{account_prefix}{self.number}"
        check_digits = '{:02d}'.format(98 - (int(iban) * 100 % 97))

        iban = f"{country_code}{check_digits}{bank_code}{account_prefix}{self.number}"
        return iban
