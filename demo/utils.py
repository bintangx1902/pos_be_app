import random, string


def slug_generator(num):
    letter = string.ascii_letters
    number = '0123456789'
    raw = number + letter
    return ''.join(random.sample(raw, num))


def check_link(links: list, num: int, link):
    while True:
        if link in links:
            new_link = slug_generator(num)
            return new_link
        else:
            break
