from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from banking.common import DEFAULT_BALANCE
from banking.models.account import Account
from banking.utils import generate_account_number


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Account.objects.create(
            number=generate_account_number(),
            balance=DEFAULT_BALANCE,
            user=instance,
            name="Current account 1",
        )
        Account.objects.create(
            number=generate_account_number(),
            balance=DEFAULT_BALANCE,
            user=instance,
            name="Current account 2",
        )
