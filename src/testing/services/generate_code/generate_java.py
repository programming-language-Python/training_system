from random import randint, choice

from testing.services.generate_code.config import Config, get_readable_variables, get_random_i, get_step
from testing.utils.random_value import RandomValue
from testing.utils.utils import add_tabs_to_paragraphs


class GenerateJava:
    def __init__(self, **task_setup: dict) -> None:
        self.random_value = RandomValue()
        self.config = Config()
        self.code = ''
        # is_generate_OOP = True
        # if is_generate_OOP:
        #     generate_java_OOP()
        self.is_if_operator = task_setup['is_if_operator'] == 'Присутствует'
        self.condition_of_if_operator = task_setup['condition_of_if_operator']
        self.presence_one_of_cycles = task_setup['presence_one_of_cycles']
        self.cycle_condition = task_setup['cycle_condition']
        self.operator_nesting = task_setup['operator_nesting']

        self.count_variables = ''
        self.variables = get_readable_variables()
        self.initialized_variables = {}
        self.generate_initialized_variables()

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

        self.boolean_expression = ''
        self.body = ''
        self.boolean_expression_and_body = ''
        self.for_cycle = ''
        self.condition = ''
        self.cycle = ''
        self.nested_operator = ''
        self.generate_code()

    def generate_initialized_variables(self) -> None:
        self.count_variables = randint(2, 3)
        for i in range(self.count_variables):
            random_variable = choice(self.variables)
            self.initialized_variables[random_variable] = self.random_value.get_random_positive_int()
            # self.initialized_variables[random_variable] = 80
            self.variables = self.variables.replace(random_variable, '')

    def generate_code(self) -> None:
        self.generate_variables()
        if self.operator_nesting:
            self.generate_nesting_of_operators()
        elif self.is_if_operator and self.presence_one_of_cycles:
            self.generate_condition_and_cycle()
        elif self.is_if_operator:
            self.generate_condition()
            self.code += self.condition
        elif self.presence_one_of_cycles:
            self.generate_cycle()
            self.code += self.cycle
        # self.code = f'#variables_used_info:{self.variables_used_info}\n' + self.code
        self.generate_print_of_variable()

    def generate_variables(self) -> None:
        # variables_used = f'#variables_used:'
        for key, value in self.initialized_variables.items():
            # variables_used += f'{key} '

            self.variables_used_info['type'] = 'int'
            self.variables_used_info['value'] = value

            self.code += f'int {key} = {value};\n'
        # self.code = variables_used + '\n' + self.code

    def generate_nesting_of_operators(self) -> None:
        operator_nesting = choice(self.operator_nesting).title
        if operator_nesting == 'оператор if вложен в цикл':
            self.generate_condition()
            self.nested_operator = self.condition
            self.generate_cycle()
            self.code += self.cycle
        else:
            self.generate_cycle()
            self.nested_operator = self.cycle
            self.generate_condition()
            self.code += self.condition

    def generate_cycle(self) -> None:
        operator = choice(self.presence_one_of_cycles).title
        if operator == 'for':
            self.generate_for_with_body()
        else:
            self.generate_boolean_expression_and_body(operator)
            self.cycle = self.boolean_expression_and_body

    def generate_for_with_body(self) -> None:
        if self.cycle_condition == 'Составное':
            self.generate_compound_for_cycle()
            self.generate_body(is_random_variables=False)
        else:
            self.generate_simple_for_cycle()
            self.generate_body()
        self.cycle = self.for_cycle + self.body + '\n'
        if self.nested_operator:
            nested_operator = add_tabs_to_paragraphs(self.nested_operator)
            self.cycle += nested_operator
        self.cycle += '}'

    def generate_body(self, is_random_variables: bool = True) -> None:
        if is_random_variables:
            self.generate_body_with_random_variables()
        else:
            self.generate_body_with_variables_bound_to_arithmetic_operators()

    def generate_body_with_random_variables(self) -> None:
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        random_arithmetic_operator = choice(Config.ARITHMETIC_OPERATORS)
        assignment_operator = self.random_value.get_assignment_operator(random_variable, random_arithmetic_operator)
        self.add_variable_used_info(random_variable, random_arithmetic_operator)
        self.body = f'\t{assignment_operator}'

    def add_variable_used_info(self, variable: str, arithmetic_operator: str) -> None:
        if variable in self.variables_used_info:
            self.variables_used_info[variable].append(arithmetic_operator)
        else:
            self.variables_used_info[variable] = [arithmetic_operator]

    def generate_body_with_variables_bound_to_arithmetic_operators(self):
        self.body = ''
        i = 1
        for variable, arithmetic_operators in self.variables_bound_to_arithmetic_operators.items():
            if arithmetic_operators:
                random_arithmetic_operator = choice(arithmetic_operators)
            else:
                random_arithmetic_operator = choice(Config.ARITHMETIC_OPERATORS)
            assignment_operator = self.random_value.get_assignment_operator(variable, random_arithmetic_operator)
            self.body += f'\t{assignment_operator}'
            is_last_variable = i != self.count_variables
            if is_last_variable:
                self.body += '\n'
            i += 1
            self.add_variable_used_info(variable, random_arithmetic_operator)

    def generate_compound_for_cycle(self) -> None:
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        random_comparison_operator2 = choice(Config.COMPARISON_OPERATORS)
        self.add_variable_bound_to_arithmetic_operator(random_variable, random_comparison_operator2)
        i = get_random_i()
        greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        random_comparison_operator = self.random_value.get_random_dictionary_key(greater_and_less_comparison_operators)
        max_i = get_random_i()
        random_logical_operator = choice(Config.LOGICAL_OPERATORS)
        rand_int = self.random_value.get_random_positive_int()
        arithmetic_operators = Config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[random_comparison_operator]
        random_arithmetic_operator = choice(arithmetic_operators)
        step = get_step()

        self.variables_used_info['comparison_operator_in_loop'] = random_comparison_operator2

        self.for_cycle = f'for (int i = {i}; i {random_comparison_operator} {max_i} {random_logical_operator} ' \
                         f'{random_variable} {random_comparison_operator2} {rand_int}; ' \
                         f'i {random_arithmetic_operator}= {step}) ' + '{\n'

    def generate_simple_for_cycle(self):
        i = self.random_value.get_random_positive_int()
        max_i = self.random_value.get_random_positive_int()
        step = self.random_value.get_random_positive_int()
        random_comparison_operator = choice(['<', '<='])
        self.for_cycle = f'for (int i = {i}; i {random_comparison_operator} {max_i}; i += {step}) ' + '{\n'

    def generate_boolean_expression_and_body(self, operator):
        self.boolean_expression_and_body = ''
        if operator == 'if':
            self.generate_body()
            self.generate_boolean_expression(operator, self.condition_of_if_operator)
        else:
            self.generate_boolean_expression(operator, self.cycle_condition)
            self.generate_body(is_random_variables=False)
        if operator == 'do-while':
            self.boolean_expression_and_body += 'do {\n' + self.body
            if self.nested_operator:
                nested_operator = add_tabs_to_paragraphs(self.nested_operator)
                self.boolean_expression_and_body += '\n' + nested_operator
            self.boolean_expression_and_body += '\n}\n' + f'while {self.boolean_expression};'
        else:
            self.boolean_expression_and_body = operator + ' ' + self.boolean_expression + ' ' + '{\n' + self.body
            if self.nested_operator:
                nested_operator = add_tabs_to_paragraphs(self.nested_operator)
                self.boolean_expression_and_body += '\n' + nested_operator
            self.boolean_expression_and_body += '\n}'

    def generate_boolean_expression(self, operator, condition):
        if condition == 'Составное':
            self.generate_compound_boolean_expression(operator)
            return
        self.generate_simple_boolean_expression(operator)

    def generate_compound_boolean_expression(self, operator):
        self.boolean_expression = ''
        i = 1
        is_while_or_do_while_cycle = operator == 'while' or operator == 'do-while'
        if is_while_or_do_while_cycle:
            greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
        for variable in self.initialized_variables.keys():
            if operator == 'if':
                random_comparison_operator = choice(Config.COMPARISON_OPERATORS)
            else:
                random_comparison_operator = self.random_value.get_random_dictionary_key(
                    greater_and_less_comparison_operators)
                self.config.add_arithmetic_operator_used(random_comparison_operator)
                self.add_variable_bound_to_arithmetic_operator(variable, random_comparison_operator)
            rand_int = self.random_value.get_random_positive_int()
            logical_operator = choice(Config.LOGICAL_OPERATORS)
            variable_comparison = f'{variable} {random_comparison_operator} {rand_int}'
            if i == self.count_variables:
                self.boolean_expression = f'(' + self.boolean_expression + f'{variable_comparison})'
            else:
                self.boolean_expression += f'{variable_comparison} {logical_operator} '
            i += 1

    def generate_simple_boolean_expression(self, operator):
        random_variable = self.random_value.get_random_dictionary_key(self.initialized_variables)
        rand_int = self.random_value.get_random_positive_int()
        if operator == 'if':
            random_comparison_operator = choice(Config.COMPARISON_OPERATORS)
        else:
            greater_and_less_comparison_operators = self.config.get_greater_and_less_comparison_operators()
            random_comparison_operator = self.random_value.get_random_dictionary_key(
                greater_and_less_comparison_operators)
            self.config.add_arithmetic_operator_used(random_comparison_operator)
            self.add_variable_bound_to_arithmetic_operator(random_variable, random_comparison_operator)
        self.boolean_expression = f'({random_variable} {random_comparison_operator} {rand_int})'

    def generate_while_cycle(self):
        operator = 'while'
        self.generate_boolean_expression_and_body(operator)
        self.cycle = self.boolean_expression_and_body

    def generate_condition(self):
        operator = 'if'
        self.generate_boolean_expression_and_body(operator)
        self.condition = self.boolean_expression_and_body

    def generate_condition_and_cycle(self):
        self.generate_condition()
        self.generate_cycle()
        condition_and_cycle = [self.condition, self.cycle]
        random_index = randint(0, 1)
        self.code += condition_and_cycle.pop(random_index) + '\n' + condition_and_cycle[0]

    def generate_print_of_variable(self):
        list_variables = list(self.initialized_variables)
        random_variable = choice(list_variables)
        # self.code += f'\nSystem.out.println("{random_variable} = " + {random_variable});'
        self.code += f'\nSystem.out.println({random_variable});'

    def add_variable_bound_to_arithmetic_operator(self, variable, comparison_operator):
        self.variables_bound_to_arithmetic_operators[variable] = Config.COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[
            comparison_operator]

    def get_code(self):
        return self.code
