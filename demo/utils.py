import random, string


def slug_generator(num):
    letter = string.ascii_letters
    number = '0123456789'
    raw = number + letter
    return ''.join(random.sample(raw, num))
