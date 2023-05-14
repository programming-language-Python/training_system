from random import choice, randint, uniform

from testing.utils.utils import get_list_dictionary_keys


class RandomValue:
    def get_random_number(self) -> [int, float]:
        number_type = ['int', 'float']
        random_number_type = choice(number_type)
        if random_number_type == 'int':
            return self.get_random_int()
        else:
            return self.get_random_float()

    def get_assignment_operator(self, variable: str, arithmetic_operator: str) -> str:
        return f'{variable} {arithmetic_operator}= {self.get_random_positive_int()};'

    @staticmethod
    def get_random_dictionary_key(dictionary: dict) -> str:
        list_initialized_variables = get_list_dictionary_keys(dictionary)
        return choice(list_initialized_variables)

    # исключить рандомизацию с 0
    @staticmethod
    def get_random_int() -> int:
        return randint(-100, 100)

    @staticmethod
    def get_random_float() -> float:
        return round(uniform(-100, 100), 2)

    @staticmethod
    def get_random_positive_int() -> int:
        return randint(1, 100)
