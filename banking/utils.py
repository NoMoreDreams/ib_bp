import random

from banking.models.account import Account


def generate_account_number() -> str:
    random_number = "{:010d}".format(random.randint(0, 9999999999))

    if random_number in [account.number for account in Account.objects.all()]:
        return generate_account_number()
    else:
        return random_number


def generate_payment_pin() -> str:
    return "{:06d}".format(random.randint(0, 999999))
