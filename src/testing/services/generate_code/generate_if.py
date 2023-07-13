from random import choice

from testing.services.generate_code import abstractions
from testing.services.generate_code.config import COMPARISON_OPERATORS, \
    LOGICAL_OPERATORS, ARITHMETIC_OPERATORS
from testing.services.generate_code.interfaces import IBody, ICondition, \
    ICompoundCondition
from testing.services.generate_code.types import ConditionType
from testing.utils.random_value import get_positive_int


class GenerateIf(abstractions.Variable, IBody, ICondition, ICompoundCondition):
    def execute(self, condition_type: ConditionType) -> str:
        condition = self._get_condition(condition_type)
        body = self._generate_body()
        template = f'''
if ({condition}){'{'}
    {body}
{'}'}'''
        return template

    #
    def _generate_body(self):
        variable = self.get_random_used_variable()
        # TODO Расскоментить
        value = get_positive_int()
        # value = 100
        arithmetic_operation = choice(ARITHMETIC_OPERATORS)
        # arithmetic_operation = choice(['-', '/'])
        body = f'{variable} {arithmetic_operation}= {value};'

        self.set_value_in_condition(
            name=variable,
            value=value
        )
        self.set_arithmetic_operation_in_condition(
            name=variable,
            arithmetic_operation=arithmetic_operation
        )

        return body

    def _get_condition(self, condition_type: ConditionType) -> str:
        is_simple = condition_type == ConditionType.SIMPLE
        if is_simple:
            variable = self.get_random_used_variable()
            return self._generate_simple_condition(variable)
        return self._generate_compound_condition()

    @staticmethod
    def _generate_simple_condition(variable: str) -> str:
        comparison_operator = choice(COMPARISON_OPERATORS)
        value = get_positive_int()
        simple_condition = f'{variable} {comparison_operator} {value}'
        return simple_condition

    def _generate_compound_condition(self) -> str:
        condition = ''
        i = 1
        for variable in self.info.keys():
            condition = self._generate_condition(variable, i, condition)
            i += 1
        return condition

    def _generate_condition(self, variable: str, i: int,
                            condition: str) -> str:
        simple_condition = self._generate_simple_condition(variable)
        if i == self.get_count():
            condition = f'{condition}{simple_condition}'
        else:
            logical_operator = choice(LOGICAL_OPERATORS)
            condition += f'{simple_condition} {logical_operator} '
        return condition
