from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from banking.common import DEFAULT_BALANCE
from banking.models.account import Account
from banking.models.transaction import Transaction
from banking.utils import generate_account_number


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Account.objects.create(number=generate_account_number(), balance=DEFAULT_BALANCE, user=instance)
        Account.objects.create(number=generate_account_number(), balance=DEFAULT_BALANCE, user=instance)


# @receiver(post_save, sender=Transaction)
# def create_user_account(sender, instance, created, **kwargs):
#     if created:
#         instance.
