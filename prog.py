import random

def getLotto():
    lotto_numbers = set()

    while len(lotto_numbers) < 7:
        random_number = random.randint(1, 35)
        lotto_numbers.add(random_number)

    return lotto_numbers

            