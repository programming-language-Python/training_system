from random import choice

from testing.services.generate_code import abstractions
from testing.services.generate_code.config import \
    INCREMENT_ARITHMETIC_OPERATORS, DECREMENT_ARITHMETIC_OPERATORS
from testing.services.generate_code.types import Variable


# from testing.services.generate_code.variable_service import VariableService


class CheckForLooping(abstractions.Variable, abstractions.Condition):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def check_with_condition_priority(self) -> str:
        """Возвращает изменённое условие или текущее"""
        for data in self.get_info().values():
            is_not_looping = data.arithmetic_operation_in_cycle != '*' \
                             or data.value_in_condition is None
            if is_not_looping:
                continue
            if data.value < data.value_in_condition:
                arithmetic_operator = choice(INCREMENT_ARITHMETIC_OPERATORS)
                return self._get_new_condition(data, arithmetic_operator)
            if data.value == data.value_in_condition:
                arithmetic_operator = choice(['+', '*', '/'])
                return self._get_new_condition(data, arithmetic_operator)
        return self.condition

    def _get_new_condition(self, variable_data: Variable,
                           arithmetic_operator: str) -> str:
        old_expression_in_if = variable_data.get_expression_in_if()
        variable = variable_data.name
        value = variable_data.value_in_condition
        new_expression_in_if = f'{variable} {arithmetic_operator}= {value}'
        new_condition = self.condition.replace(
            old_expression_in_if,
            new_expression_in_if
        )
        return new_condition

    def check_with_cycle_priority(self) -> str:
        """Возвращает изменённое условие или текущее"""
        for data in self.get_info().values():
            is_empty_value_in_operator = data.value_in_cycle is None \
                                         or data.value_in_condition is None
            if is_empty_value_in_operator:
                continue
            if self._is_looping_1(data):
                arithmetic_operator = choice(['*', '-', '/'])
                return self._get_new_condition(data, arithmetic_operator)
            if self._is_looping_2(data):
                arithmetic_operator = choice(INCREMENT_ARITHMETIC_OPERATORS)
                return self._get_new_condition(data, arithmetic_operator)
        return self.condition

    @staticmethod
    def _is_looping_1(data: Variable) -> bool:
        arithmetic_operation_in_cycle = data.arithmetic_operation_in_cycle
        arithmetic_operation_in_condition = \
            data.arithmetic_operation_in_condition
        value_in_cycle = data.value_in_cycle
        value_in_condition = data.value_in_condition

        is_looping_1 = (
                arithmetic_operation_in_cycle == '-'
                and arithmetic_operation_in_condition == '+'
                and (
                        value_in_cycle < value_in_condition
                        or value_in_cycle == value_in_condition
                )
        )
        return is_looping_1

    @staticmethod
    def _is_looping_2(data: Variable) -> bool:
        arithmetic_operation_in_cycle = data.arithmetic_operation_in_cycle
        arithmetic_operation_in_condition = \
            data.arithmetic_operation_in_condition
        value_in_cycle = data.value_in_cycle
        value_in_condition = data.value_in_condition

        is_looping_2 = (
                arithmetic_operation_in_cycle == '+'
                and arithmetic_operation_in_condition
                in DECREMENT_ARITHMETIC_OPERATORS
                and (
                        value_in_cycle < value_in_condition
                        or value_in_cycle == value_in_condition
                )
        )
        return is_looping_2
