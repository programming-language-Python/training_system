from random import randint, choice

from testing.utils.random_value import RandomValue
from testing.utils.utils import add_tabs_to_paragraphs, remove_empty_paragraphs
from .generate_if import GenerateIf
from .generate_java_OOP import GenerateJavaOOP
from .generate_java_string import GenerateJavaString

from dataclasses import dataclass


# TODO надо разделить код на части
@dataclass
class Variable:
    name: str
    data_type: str
    value: int
    value_in_cycle: int = None
    value_in_condition: int = None
    arithmetic_operation_in_cycle: str = None
    arithmetic_operation_in_condition: str = None

    def get_expression_in_if(self):
        return f'{self.name} {self.arithmetic_operation_in_condition}= {self.value_in_condition}'


# TODO add_arithmetic_operator_used она нужна?

class GenerateJava:
    body: str = ''

    def __init__(self, config) -> None:
        self.random_value = RandomValue()
        self.config = config

    def execute(self) -> str:
        code = ''
        if self.config.is_OOP:
            return self.get_java_OOP()
        if self.config.is_strings:
            return self.get_java_string()
        code += self.generate_variables()
        if self.config.operator_nesting:
            code += self.generate_nesting_of_operators()
        else:
            code += self.get_operator()
        code += self.generate_print_of_variable()
        return remove_empty_paragraphs(code)

    @staticmethod
    def get_java_OOP():
        generate_java_OOP = GenerateJavaOOP()
        return generate_java_OOP.execute()

    @staticmethod
    def get_java_string():
        generate_java_string = GenerateJavaString()
        generate_java_string.execute()
        return generate_java_string.get_code()

    # TODO generate_variables и generate_initialized_variables можно объединить
    def generate_variables(self) -> str:
        variables = ''
        self.generate_initialized_variables()
        data_type = 'int'
        for name, value in self.config.initialized_variables.items():
            variables += f'{data_type} {name} = {value};\n'

            self.config.variables_info[name] = Variable(name, data_type, value)
        return variables

    def generate_initialized_variables(self) -> None:
        # TODO Расскоментить
        # self.count_variables = randint(2, 3)
        self.config.count_variables = 1
        for i in range(self.config.count_variables):
            variable = choice(self.config.variables)
            self.config.initialized_variables[variable] = self.random_value.get_positive_int()
            # self.initialized_variables[random_variable] = 80
            self.config.variables = self.config.variables.replace(variable, '')

    def generate_nesting_of_operators(self) -> str:
        operator_nesting = choice(self.config.operator_nesting).title
        if operator_nesting == 'оператор if вложен в цикл':
            return self.generate_cycle(nested_operator=self.generate_if())
        return self.generate_if(nested_operator=self.generate_cycle())

    def get_operator(self) -> str:
        operators = ''
        if self.config.is_if_operator:
            generate_if = GenerateIf()
            operators += generate_if.execute()
        if self.config.presence_one_of_cycles:
            operators += self.generate_cycle()
        return operators

    def generate_cycle(self, nested_operator: str = '') -> str:
        operator = choice(self.config.presence_one_of_cycles).title
        if operator == 'while':
            return self.generate_while(nested_operator=nested_operator)
        if operator == 'do-while':
            return self.generate_do_while(nested_operator=nested_operator)
        if operator == 'for':
            return self.generate_for(nested_operator=nested_operator)

    def generate_while(self, nested_operator: str = '') -> str:
        if self.config.cycle_condition == 'Простое':
            condition = self._generate_simple_condition_for_while()
        else:
            condition = self._generate_compound_condition_for_while()
        body = self._generate_body_for_while()
        template_while = f'''
while ({condition}){'{'}
    {body}
    {add_tabs_to_paragraphs(nested_operator)}
{'}'}'''
        return template_while

    def _generate_simple_condition_for_while(self) -> str:
        variable = self.get_random_initialized_variable()
        rand_int = self.random_value.get_positive_int()
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        # TODO Расскоментить
        comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
        # comparison_operator = '<'
        # self.config.add_arithmetic_operator_used(comparison_operator)
        self.add_variable_bound_to_arithmetic_operator(variable, comparison_operator)
        return f'{variable} {comparison_operator} {rand_int}'

    def add_variable_bound_to_arithmetic_operator(self, variable, comparison_operator):
        self.config.variables_bound_to_arithmetic_operators[variable] = \
        self.config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[
            comparison_operator]

    def _generate_compound_condition_for_while(self) -> str:
        condition = ''
        i = 1
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        for variable in self.config.initialized_variables.keys():
            comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
            # self.config.add_arithmetic_operator_used(comparison_operator)
            self.add_variable_bound_to_arithmetic_operator(variable, comparison_operator)
            rand_int = self.random_value.get_positive_int()
            logical_operator = choice(self.config.LOGICAL_OPERATORS)
            variable_comparison = f'{variable} {comparison_operator} {rand_int}'
            if i == self.config.count_variables:
                condition = f'{condition}{variable_comparison}'
            else:
                condition += f'{variable_comparison} {logical_operator} '
            i += 1
        return condition

    def _generate_body_for_while(self, nested_operator: str = '') -> str:
        if nested_operator:
            for variable, data in self.config.variables_info.items():
                # TODO проверка на None?
                if data.arithmetic_operation_in_cycle == '-' \
                        and data.arithmetic_operation_in_condition == '+' \
                        and (
                        data.value_in_cycle < data.value_in_condition
                        or data.value_in_cycle == data.value_in_condition):
                    pass
                if data.arithmetic_operation_in_cycle == '+' \
                        and data.arithmetic_operation_in_condition in ['-', '/'] \
                        and (
                        data.value_in_cycle < data.value_in_condition
                        or data.value_in_cycle == data.value_in_condition):
                    pass
        else:
            return self._generate_body_with_variables_bound_to_arithmetic_operators()

    def _generate_body_with_variables_bound_to_arithmetic_operators(self) -> str:
        cycle_body = ''
        i = 1
        for variable, arithmetic_operators in self.config.variables_bound_to_arithmetic_operators.items():
            arithmetic_operator = choice(arithmetic_operators) if arithmetic_operators else choice(
                self.config.ARITHMETIC_OPERATORS)
            value = self.random_value.get_positive_int()
            assignment_operator = f'{variable} {arithmetic_operator}= {value};'
            cycle_body += f'{assignment_operator}'
            is_last_variable = i != self.config.count_variables
            cycle_body += '\n\t' if is_last_variable else ''
            i += 1
            self.config.variables_info[variable].value_in_cycle = value
            self.config.variables_info[variable].arithmetic_operation_in_cycle = arithmetic_operator
        return cycle_body

    def generate_do_while(self, nested_operator: str = '') -> str:
        if self.config.cycle_condition == 'Простое':
            condition = self._generate_simple_condition_for_while()
        else:
            condition = self._generate_compound_condition_for_while()
        body = self._generate_body_with_variables_bound_to_arithmetic_operators()
        template_do_while = f'''
do {'{'} 
    {body}
    {add_tabs_to_paragraphs(nested_operator)}
{'}'}
while ({condition});'''
        return template_do_while

    def generate_for(self, nested_operator: str = '') -> str:
        if self.config.cycle_condition == 'Простое':
            condition = self._generate_simple_condition_for()
            # TODO используется в for.
            #  _generate_body используется ещё в if.
            #  Можно разделить генерацию тела для for и для if
            body = self._generate_body()
        else:
            condition = self._generate_compound_condition_for()
            body = self._generate_body_with_variables_bound_to_arithmetic_operators()
        template_for = f'''
for ({condition}) {'{'} 
    {body}
    {add_tabs_to_paragraphs(nested_operator)}
{'}'}'''
        return template_for

    def _generate_simple_condition_for(self) -> str:
        i = self.random_value.get_random_i()
        max_i = self.random_value.get_random_i()
        step = self.random_value.get_step()
        comparison_operator = choice(['<', '<='])
        return f'int i = {i}; i {comparison_operator} {max_i}; i += {step}'

    def _generate_body(self) -> str:
        variable = self.get_random_initialized_variable()
        arithmetic_operator = choice(self.config.ARITHMETIC_OPERATORS)
        value = self.random_value.get_positive_int()
        assignment_operator = f'{variable} {arithmetic_operator}= {value};'
        # self.add_variable_info(variable, arithmetic_operator)

        self.config.variables_info[variable].value_in_condition = value
        self.config.variables_info[variable].arithmetic_operation_in_condition = arithmetic_operator
        return f'{assignment_operator}'

    def _generate_compound_condition_for(self) -> str:
        variable = self.get_random_initialized_variable()
        comparison_operator2 = choice(self.config.COMPARISON_OPERATORS)
        self.add_variable_bound_to_arithmetic_operator(variable, comparison_operator2)
        i = self.random_value.get_random_i()
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
        max_i = self.random_value.get_random_i()
        logical_operator = choice(self.config.LOGICAL_OPERATORS)
        rand_int = self.random_value.get_positive_int()
        arithmetic_operators = self.config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[comparison_operator]
        arithmetic_operator = choice(arithmetic_operators)
        step = self.random_value.get_step()
        return f'int i = {i}; i {comparison_operator} {max_i} {logical_operator} ' \
               f'{variable} {comparison_operator2} {rand_int}; ' \
               f'i {arithmetic_operator}= {step}'

    def get_random_initialized_variable(self):
        return self.random_value.get_random_dictionary_key(self.config.initialized_variables)

    def generate_print_of_variable(self):
        list_variables = list(self.config.initialized_variables)
        random_variable = choice(list_variables)
        return f'\nSystem.out.println({random_variable});'
