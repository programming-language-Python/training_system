from random import choice

from apps.testing_by_code import abstractions
from apps.testing_by_code.interfaces import ICompoundCondition, ICondition, ISimpleCondition
from apps.testing_by_code.services.generate_code.config import \
    get_greater_and_less_comparison_operators, LOGICAL_OPERATORS, ARITHMETIC_OPERATORS
from apps.testing_by_code.types import ConditionType
from apps.testing_by_code.utils.random_value import get_positive_int, \
    get_random_dictionary_key


class GenerateWhile(abstractions.Variable, ICondition, ISimpleCondition,
                    ICompoundCondition):
    def execute(self, condition_type: ConditionType) -> str:
        condition = self._get_condition(condition_type)
        body = self._generate_body_with_variables_bound_to_arithmetic_operators()
        template = f'''
while ({condition}){'{'}
    {body}
{'}'}'''
        return template

    def _get_condition(self, condition_type: ConditionType) -> str:
        is_simple = condition_type == ConditionType.SIMPLE
        if is_simple:
            return self._generate_simple_condition()
        return self._generate_compound_condition()

    def _generate_simple_condition(self) -> str:
        variable = self.get_random_used_variable()
        greater_and_less_comparison_operators = \
            get_greater_and_less_comparison_operators()
        # # TODO Расскоментить
        comparison_operator = get_random_dictionary_key(
            greater_and_less_comparison_operators
        )
        # comparison_operator = '<'
        value = get_positive_int()
        # value = 10

        self.set_arithmetic_operation_in_cycle_having_comparison_operator(
            name=variable,
            comparison_operator=comparison_operator
        )

        return f'{variable} {comparison_operator} {value}'

    # TODO отрефакторить
    def _generate_compound_condition(self) -> str:
        condition = ''
        i = 1
        greater_and_less_comparison_operators = \
            get_greater_and_less_comparison_operators()
        for variable in self.get_info().keys():
            comparison_operator = get_random_dictionary_key(
                greater_and_less_comparison_operators
            )
            value = get_positive_int()
            variable_comparison = f'{variable} {comparison_operator} {value}'
            is_last_variable = i == self.get_count()
            if is_last_variable:
                condition = f'{condition}{variable_comparison}'
            else:
                logical_operator = choice(LOGICAL_OPERATORS)
                condition += f'{variable_comparison} {logical_operator} '
            i += 1
            self.set_arithmetic_operation_in_cycle_having_comparison_operator(
                name=variable,
                comparison_operator=comparison_operator
            )
        return condition

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
