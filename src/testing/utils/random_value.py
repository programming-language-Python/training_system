from random import choice, randint, uniform

from testing.utils.utils import get_list_dictionary_keys


class RandomValue:
    MAX_NUMBER = 100
    MIN_NUMBER = -100
    MAX_DIGIT = 9
    MIN_DIGIT = 0
    MAX_N_DIGIT_NUMBER = 999999

    def get_number(self) -> [int, float]:
        number_type = ['int', 'float']
        random_number_type = choice(number_type)
        if random_number_type == 'int':
            return self.get_int()
        else:
            return self.get_float()

    def get_N_digits(self) -> int:
        return randint(self.MIN_DIGIT, self.MAX_N_DIGIT_NUMBER)

    @staticmethod
    def get_number_in_range(end: int, start: int = 0) -> int:
        return randint(start, end)

    def get_digit(self):
        return randint(self.MIN_DIGIT, self.MAX_DIGIT)

    @staticmethod
    def get_random_dictionary_key(dictionary: dict) -> str:
        return choice(get_list_dictionary_keys(dictionary))

    # TODO исключить рандомизацию с 0
    def get_int(self) -> int:
        return randint(self.MIN_NUMBER, self.MAX_NUMBER)

    def get_float(self) -> float:
        return round(uniform(self.MIN_NUMBER, self.MAX_NUMBER), 2)

    def get_positive_int(self) -> int:
        return randint(1, self.MAX_NUMBER)

    def get_positive_int_for_value_variable(self) -> int:
        return randint(2, self.MAX_NUMBER)

    def get_positive_result_from_zero(self) -> int:
        return randint(self.MIN_DIGIT, self.MAX_NUMBER)

    @staticmethod
    def get_random_i() -> int:
        return randint(0, 10)

    @staticmethod
    def get_step() -> int:
        return randint(1, 2)
