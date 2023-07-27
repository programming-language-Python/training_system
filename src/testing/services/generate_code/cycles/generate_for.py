from random import choice

from testing import abstractions
from testing.interfaces import IBody, ISimpleCondition, ICompoundCondition
from testing.services.generate_code.check_for_looping import check_step
from testing.services.generate_code.config import COMPARISON_OPERATORS, \
    LOGICAL_OPERATORS, get_greater_and_less_comparison_operators, \
    COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS, ARITHMETIC_OPERATORS
from testing.types import ConditionType
from testing.utils.random_value import get_i, get_step, \
    get_random_dictionary_key, get_positive_int


class GenerateFor(abstractions.Variable, IBody, ISimpleCondition,
                  ICompoundCondition):
    def execute(self, condition_type: ConditionType) -> str:
        is_simple = condition_type == ConditionType.SIMPLE
        if is_simple:
            condition = self._generate_simple_condition()
            body = self._generate_body()
        else:
            condition = self._generate_compound_condition()
            body = self._generate_body_with_variables_bound_to_arithmetic_operators()

        template = f'''
for ({condition}) {'{'} 
    {body}
{'}'}'''
        return template

    @staticmethod
    def _generate_simple_condition() -> str:
        i = get_i()
        max_i = get_i()
        step = get_step()
        comparison_operator = choice(['<', '<='])
        return f'int i = {i}; i {comparison_operator} {max_i}; i += {step}'

    def _generate_body(self) -> str:
        variable = self.get_random_used_variable()
        # TODO Расскоментить
        value = get_positive_int()
        # value = 100
        arithmetic_operation = choice(ARITHMETIC_OPERATORS)
        # arithmetic_operation = choice(['-', '/'])
        body = f'{variable} {arithmetic_operation}= {value};'

        self.set_value_in_cycle(
            name=variable,
            value=value
        )
        self.set_arithmetic_operation_in_cycle(
            name=variable,
            arithmetic_operation=arithmetic_operation
        )

        return body

    def _generate_compound_condition(self) -> str:
        i = get_i()
        comparison_operator = self._get_comparison_operator()
        max_i = get_i()
        logical_operator = choice(LOGICAL_OPERATORS)
        variable = self.get_random_used_variable()
        comparison_operator2 = choice(COMPARISON_OPERATORS)
        value = get_positive_int()
        arithmetic_operator = self._get_arithmetic_operator(
            comparison_operator
        )
        step = check_step(arithmetic_operator)
        compound_condition = f'int i = {i}; ' \
                             f'i {comparison_operator} {max_i} ' \
                             f'{logical_operator} ' \
                             f'{variable} {comparison_operator2} {value}; ' \
                             f'i {arithmetic_operator}= {step}'
        self.set_arithmetic_operation_in_cycle_having_comparison_operator(
            name=variable,
            comparison_operator=comparison_operator2
        )
        return compound_condition

    @staticmethod
    def _get_comparison_operator() -> str:
        greater_and_less_comparison_operators = \
            get_greater_and_less_comparison_operators()
        comparison_operator = get_random_dictionary_key(
            greater_and_less_comparison_operators
        )
        return comparison_operator

    @staticmethod
    def _get_arithmetic_operator(comparison_operator: str) -> str:
        arithmetic_operators = COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[
            comparison_operator
        ]
        arithmetic_operator = choice(arithmetic_operators)
        return arithmetic_operator

    def _generate_body_with_variables_bound_to_arithmetic_operators(self):
        body = ''
        i = 1
        for variable, info in self.info.items():
            arithmetic_operator_in_cycle = info.arithmetic_operation_in_cycle
            arithmetic_operator = self._get_random_arithmetic_operator(arithmetic_operator_in_cycle)
            value = get_positive_int()
            assignment_operator = f'{variable} {arithmetic_operator}= {value};'

            body += assignment_operator
            is_last_variable = i != self.get_count()
            body += '\n\t' if is_last_variable else ''
            i += 1

            self.set_value_in_cycle(variable, value)
        return body

    @staticmethod
    def _get_random_arithmetic_operator(arithmetic_operators) -> str:
        if arithmetic_operators:
            return choice(arithmetic_operators)
        else:
            return choice(ARITHMETIC_OPERATORS)
