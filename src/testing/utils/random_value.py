from random import choice, randint, uniform


class RandomValue:
    def get_random_number(self) -> [int, float]:
        number_type = ['int', 'float']
        random_number_type = choice(number_type)
        if random_number_type == 'int':
            return self.get_random_int()
        else:
            return self.get_random_float()

    @staticmethod
    def get_random_int() -> int:
        return randint(-100, 100)

    @staticmethod
    def get_random_float() -> float:
        return round(uniform(-100, 100), 2)

    @staticmethod
    def get_random_positive_int() -> int:
        return randint(90, 100)
