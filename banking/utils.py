import random


def generate_account_number() -> str:
    return '{:010d}'.format(random.randint(0, 9999999999))
