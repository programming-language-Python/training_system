from random import choice, randint, uniform
from typing import Mapping

from testing.utils.utils import get_list_dictionary_keys

MAX_NUMBER = 100
MIN_NUMBER = -100
MAX_DIGIT = 9
MIN_DIGIT = 0
MAX_N_DIGIT_NUMBER = 999999


def get_number() -> [int, float]:
    number_type = ['int', 'float']
    random_number_type = choice(number_type)
    if random_number_type == 'int':
        return get_int()
    else:
        return get_float()


def get_N_digits() -> int:
    return randint(MIN_DIGIT, MAX_N_DIGIT_NUMBER)


def get_number_in_range(end: int, start: int = 0) -> int:
    return randint(start, end)


def get_digit():
    return randint(MIN_DIGIT, MAX_DIGIT)


def get_random_dictionary_key(dictionary: Mapping) -> str:
    return choice(get_list_dictionary_keys(dictionary))


def get_int() -> int:
    while True:
        number = randint(MIN_NUMBER, MAX_NUMBER)
        if number != 0:
            break
    return number


def get_float() -> float:
    return round(uniform(MIN_NUMBER, MAX_NUMBER), 2)


def get_positive_int() -> int:
    return randint(1, MAX_NUMBER)


def get_positive_int_for_value_variable() -> int:
    return randint(2, MAX_NUMBER)


def get_positive_result_from_zero() -> int:
    return randint(MIN_DIGIT, MAX_NUMBER)


def get_i() -> int:
    return randint(0, 10)


def get_step() -> int:
    return randint(1, 10)


def get_step_starting_from_2() -> int:
    return randint(2, 10)
