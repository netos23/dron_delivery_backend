import random


def remove_none(original):
    return {k: v for k, v in original.items() if v is not None}


def sms_code_generator(digits=3):
    return str(random.randint(10 ** (digits - 1) + 1, 10**digits - 1))
