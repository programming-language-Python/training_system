import string
from random import randint, choice


def get_readable_variables() -> str:
    variables = string.ascii_letters
    excluded_variables = ['i', 'l', 'o', 'O']
    for variable in excluded_variables:
        variables = variables.replace(variable, '')
    return variables


def get_random_i():
    return randint(0, 10)


def get_step():
    return randint(1, 2)


class Config:
    INTEGER_DATA_TYPES = ['byte', 'short', 'int', 'long']
    REAL_DATA_TYPES = ['float', 'double']
    NUMERIC_DATA_TYPES = INTEGER_DATA_TYPES + REAL_DATA_TYPES
    COMPARISON_OPERATORS = ['<', '<=', '>', '>=', '==', '!=']
    LOGICAL_OPERATORS = ['&&', '||']
    INCREMENT_ARITHMETIC_OPERATORS = ['+', '*']
    DECREMENT_ARITHMETIC_OPERATORS = ['-', '/']
    ARITHMETIC_OPERATORS = INCREMENT_ARITHMETIC_OPERATORS + DECREMENT_ARITHMETIC_OPERATORS
    # TODO Скорее всего удалить
    # arithmetic_operators_used = []
    arithmetic_operator = ''
    COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS = {
        '<': INCREMENT_ARITHMETIC_OPERATORS,
        '<=': INCREMENT_ARITHMETIC_OPERATORS,
        '>': DECREMENT_ARITHMETIC_OPERATORS,
        '>=': DECREMENT_ARITHMETIC_OPERATORS,
        '==': '',
        '!=': ''
    }

    def __init__(self):
        self.variables = get_readable_variables()

    def get_random_variable(self) -> str:
        random_variable = choice(self.variables)
        self.variables = self.variables.replace(random_variable, '')
        return random_variable

    # TODO Скорее всего удалить тоже самое что и в generate_java. Я её хотел перенести сюда, но не до перенёс
    # def add_arithmetic_operator_used(self, comparison_operator):
    #     self.arithmetic_operators_used += self.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[
    #         comparison_operator]

    def get_greater_and_less_comparison_operators(self) -> dict:
        greater_and_less_comparison_operators = self.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS.copy()
        del greater_and_less_comparison_operators['==']
        del greater_and_less_comparison_operators['!=']
        return greater_and_less_comparison_operators
