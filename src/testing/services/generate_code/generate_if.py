from random import choice

from testing.services.generate_code.config import Config
from testing.services.generate_code.generate_java import GenerateJava
from testing.utils.utils import add_tabs_to_paragraphs


class GenerateIf:
    def execute(self, nested_operator: str = '') -> str:
        if self.condition_of_if_operator == 'Простое':
            condition = self._generate_simple_condition(variable=self.get_random_initialized_variable())
        else:
            condition = self._generate_compound_condition()

        variable = self.get_random_initialized_variable()
        value = self.random_value.get_positive_int()

        self.variables_info[variable].value_in_condition = value
        body = f'{variable} {self.get_arithmetic_operator(nested_operator)}= {value};'
        template_if = f'''
    if ({condition}){'{'}
        {body}
        {add_tabs_to_paragraphs(nested_operator)}
    {'}'}'''
        return template_if

    def get_arithmetic_operator(self, nested_operator='') -> str:
        if nested_operator:
            for variable, data in self.variables_info.items():
                # TODO проверка на None?
                if data.arithmetic_operation_in_cycle == '*' and data.value < data.value_in_condition:
                    return choice(Config.INCREMENT_ARITHMETIC_OPERATORS)
                if data.arithmetic_operation_in_cycle == '*' and data.value == data.value_in_condition:
                    return choice(['+', '*', '/'])
        else:
            return choice(Config.ARITHMETIC_OPERATORS)

    def _generate_simple_condition(self, variable: str) -> str:
        comparison_operator = choice(Config.COMPARISON_OPERATORS)
        rand_int = self.random_value.get_positive_int()
        return f'{variable} {comparison_operator} {rand_int}'

    def _generate_compound_condition(self) -> str:
        condition = ''
        i = 1
        for variable in self.initialized_variables.keys():
            condition = self._generate_condition(variable, i, condition)
            i += 1
        return condition

    def _generate_condition(self, variable: str, i: int, condition: str) -> str:
        simple_condition = self._generate_simple_condition(variable)
        if i == self.count_variables:
            condition = f'{condition}{simple_condition}'
        else:
            logical_operator = choice(Config.LOGICAL_OPERATORS)
            condition += f'{simple_condition} {logical_operator} '
        return condition
