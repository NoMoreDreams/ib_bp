from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from banking.models.account import Account


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        iban = "your-iban-generator-function"
        balance = 100000.00
        account = Account.objects.create(iban=iban, balance=balance, user=instance)
        account.save()
