from random import randint, choice

from testing.services.generate_code.config import Config, get_readable_variables, get_random_i, get_step
from testing.utils.random_value import RandomValue
from testing.utils.utils import add_tabs_to_paragraphs, remove_empty_paragraphs
from .generate_java_OOP import GenerateJavaOOP
from .generate_java_string import GenerateJavaString


class GenerateJava:
    body: str = ''

    def __init__(self, **task_setup: dict[str, dict]) -> None:
        self.random_value = RandomValue()
        self.config = Config()

        self.is_OOP = task_setup['is_OOP']
        self.is_strings = task_setup['is_strings']
        self.is_if_operator = task_setup['is_if_operator'] == 'Присутствует'
        self.condition_of_if_operator = task_setup['condition_of_if_operator']
        self.presence_one_of_cycles: dict[str, dict] = task_setup['presence_one_of_cycles']
        self.cycle_condition = task_setup['cycle_condition']
        self.operator_nesting = task_setup['operator_nesting']

        self.count_variables = ''
        self.variables = get_readable_variables()
        self.initialized_variables = {}
        # Связь: переменная -> оператор сравнения -> арифметический оператор
        self.variables_bound_to_arithmetic_operators = {}

        # 'var':
        #   'type'
        #   'value'
        #   'comparison_operator_in_loop'
        #   'expression'
        #   'arithmetic_operations':
        #       'in_condition'
        #       'in_cycle'
        self.variables_used_info = {}

    def execute(self) -> str:
        code = ''
        if self.is_OOP:
            return self.generate_java_OOP()
        if self.is_strings:
            return self.generate_java_string()
        code += self.generate_variables()
        if self.operator_nesting:
            code += self.generate_nesting_of_operators()
        else:
            code += self.generate_operator()
        code += self.generate_print_of_variable()
        return remove_empty_paragraphs(code)

    @staticmethod
    def generate_java_OOP():
        generate_java_OOP = GenerateJavaOOP()
        return generate_java_OOP.execute()

    @staticmethod
    def generate_java_string():
        generate_java_string = GenerateJavaString()
        generate_java_string.execute()
        return generate_java_string.get_code()

    def generate_variables(self) -> str:
        variables = ''
        self.generate_initialized_variables()
        # variables_used = f'#variables_used:'
        for key, value in self.initialized_variables.items():
            # variables_used += f'{key} '

            self.variables_used_info['type'] = 'int'
            self.variables_used_info['value'] = value

            variables += f'int {key} = {value};\n'
        # self.code = variables_used + '\n' + self.code
        return variables

    def generate_initialized_variables(self) -> None:
        self.count_variables = randint(2, 3)
        for i in range(self.count_variables):
            random_variable = choice(self.variables)
            self.initialized_variables[random_variable] = self.random_value.get_positive_int()
            # self.initialized_variables[random_variable] = 80
            self.variables = self.variables.replace(random_variable, '')

    def generate_nesting_of_operators(self) -> str:
        operator_nesting = choice(self.operator_nesting).title
        if operator_nesting == 'оператор if вложен в цикл':
            return self.generate_cycle(nested_operator=self.generate_if())
        return self.generate_if(nested_operator=self.generate_cycle())

    def generate_operator(self) -> str:
        operators = ''
        if self.is_if_operator:
            operators += self.generate_if()
        if self.presence_one_of_cycles:
            operators += self.generate_cycle()
        return operators

    def generate_cycle(self, nested_operator='') -> str:
        operator = choice(self.presence_one_of_cycles).title
        if operator == 'while':
            return self.generate_while(nested_operator=nested_operator)
        if operator == 'do-while':
            return self.generate_do_while(nested_operator=nested_operator)
        if operator == 'for':
            return self.generate_for(nested_operator=nested_operator)

    def generate_while(self, nested_operator='') -> str:
        if self.cycle_condition == 'Простое':
            condition = self._generate_simple_condition_for_while()
        else:
            condition = self._generate_compound_condition_for_while()
        body = self._generate_body_with_variables_bound_to_arithmetic_operators()
        template_while = f'''
while ({condition}){'{'}
    {body}
    {add_tabs_to_paragraphs(nested_operator)}
{'}'}'''
        return template_while

    def _generate_simple_condition_for_while(self) -> str:
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        rand_int = self.random_value.get_positive_int()
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        random_comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
        self.config.add_arithmetic_operator_used(random_comparison_operator)
        self.add_variable_bound_to_arithmetic_operator(random_variable, random_comparison_operator)
        return f'{random_variable} {random_comparison_operator} {rand_int}'

    def add_variable_bound_to_arithmetic_operator(self, variable, comparison_operator):
        self.variables_bound_to_arithmetic_operators[variable] = Config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[
            comparison_operator]

    def _generate_compound_condition_for_while(self) -> str:
        condition = ''
        i = 1
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        for variable in self.initialized_variables.keys():
            random_comparison_operator = self.random_value.get_random_dictionary_key(
                greater_and_less_comparison_operators)
            self.config.add_arithmetic_operator_used(random_comparison_operator)
            self.add_variable_bound_to_arithmetic_operator(variable, random_comparison_operator)
            rand_int = self.random_value.get_positive_int()
            logical_operator = choice(Config.LOGICAL_OPERATORS)
            variable_comparison = f'{variable} {random_comparison_operator} {rand_int}'
            if i == self.count_variables:
                condition = f'{condition}{variable_comparison}'
            else:
                condition += f'{variable_comparison} {logical_operator} '
            i += 1
        return condition

    def _generate_body_with_variables_bound_to_arithmetic_operators(self) -> str:
        cycle_body = ''
        i = 1
        for variable, arithmetic_operators in self.variables_bound_to_arithmetic_operators.items():
            random_arithmetic_operator = choice(arithmetic_operators) if arithmetic_operators else choice(
                Config.ARITHMETIC_OPERATORS)
            assignment_operator = self.random_value.get_assignment_operator(variable, random_arithmetic_operator)
            cycle_body += f'{assignment_operator}'
            is_last_variable = i != self.count_variables
            cycle_body += '\n\t' if is_last_variable else ''
            i += 1
            self.add_variable_used_info(variable, random_arithmetic_operator)
        return cycle_body

    def generate_do_while(self, nested_operator='') -> str:
        if self.cycle_condition == 'Простое':
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

    def generate_for(self, nested_operator='') -> str:
        if self.cycle_condition == 'Простое':
            condition = self._generate_simple_condition_for()
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

    @staticmethod
    def _generate_simple_condition_for() -> str:
        i = get_random_i()
        max_i = get_random_i()
        step = get_step()
        random_comparison_operator = choice(['<', '<='])
        return f'int i = {i}; i {random_comparison_operator} {max_i}; i += {step}'

    def _generate_body(self) -> str:
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        random_arithmetic_operator = choice(Config.ARITHMETIC_OPERATORS)
        assignment_operator = self.random_value.get_assignment_operator(random_variable, random_arithmetic_operator)
        self.add_variable_used_info(random_variable, random_arithmetic_operator)
        return f'{assignment_operator}'

    def _generate_compound_condition_for(self) -> str:
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        random_comparison_operator2 = choice(Config.COMPARISON_OPERATORS)
        self.add_variable_bound_to_arithmetic_operator(random_variable, random_comparison_operator2)
        i = get_random_i()
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        random_comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
        max_i = get_random_i()
        random_logical_operator = choice(Config.LOGICAL_OPERATORS)
        rand_int = self.random_value.get_positive_int()
        arithmetic_operators = Config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[random_comparison_operator]
        random_arithmetic_operator = choice(arithmetic_operators)
        step = get_step()

        self.variables_used_info['comparison_operator_in_loop'] = random_comparison_operator2

        return f'int i = {i}; i {random_comparison_operator} {max_i} {random_logical_operator} ' \
               f'{random_variable} {random_comparison_operator2} {rand_int}; ' \
               f'i {random_arithmetic_operator}= {step}'

    def generate_if(self, nested_operator='') -> str:
        if self.condition_of_if_operator == 'Простое':
            condition = self._generate_simple_condition_for_if()
        else:
            condition = self._generate_compound_condition_for_if()
        body = self._generate_body()
        template_if = f'''
if ({condition}){'{'}
    {body}
    {add_tabs_to_paragraphs(nested_operator)}
{'}'}'''
        return template_if

    def _generate_simple_condition_for_if(self):
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        random_comparison_operator = choice(Config.COMPARISON_OPERATORS)
        rand_int = self.random_value.get_positive_int()
        return f'{random_variable} {random_comparison_operator} {rand_int}'

    def _generate_compound_condition_for_if(self):
        condition = ''
        i = 1
        for variable in self.initialized_variables.keys():
            random_comparison_operator = choice(Config.COMPARISON_OPERATORS)
            rand_int = self.random_value.get_positive_int()
            variable_comparison = f'{variable} {random_comparison_operator} {rand_int}'
            logical_operator = choice(Config.LOGICAL_OPERATORS)
            if i == self.count_variables:
                condition = f'{condition}{variable_comparison}'
            else:
                condition += f'{variable_comparison} {logical_operator} '
            i += 1
        return condition

    def generate_print_of_variable(self):
        list_variables = list(self.initialized_variables)
        random_variable = choice(list_variables)
        return f'\nSystem.out.println({random_variable});'

    def add_variable_used_info(self, variable: str, arithmetic_operator: str) -> None:
        if variable in self.variables_used_info:
            self.variables_used_info[variable].append(arithmetic_operator)
        else:
            self.variables_used_info[variable] = [arithmetic_operator]
