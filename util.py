import random


def get_random_digit(variable_numbers, digit_capacity):
    variable_numbers = variable_numbers.copy()
    random_digit = ''

    for i in range(digit_capacity):
        random_number = random.choice(variable_numbers)
        random_number_index = variable_numbers.index(random_number)
        
        random_digit += str(random_number)
        del variable_numbers[random_number_index]

    return random_digit