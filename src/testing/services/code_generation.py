import string
from random import randint, choice


class RandomizerJava:
    def __init__(self, **task_setup):
        self.code = ''

        self.is_if_operator = task_setup['is_if_operator'] == 'Присутствует'
        self.condition_of_if_operator = task_setup['condition_of_if_operator']
        self.presence_one_of_cycles = task_setup['presence_one_of_cycles']
        self.cycle_condition = task_setup['cycle_condition']
        self.operator_nesting = task_setup['operator_nesting']

        self.count_variables = ''
        self.variables = string.ascii_letters
        self.remove_poorly_readable_variables()
        self.initialized_variables = {}
        self.generate_initialized_variables()

        self.comparison_operators = ['<', '<=', '>', '>=', '==', '!=']
        self.logical_operators = ['&&', '||']
        increment_arithmetic_operators = ['+', '*']
        decrement_arithmetic_operators = ['-', '/']
        self.arithmetic_operators = increment_arithmetic_operators + decrement_arithmetic_operators
        self.arithmetic_operators_used = []
        self.arithmetic_operator = ''
        self.comparison_and_their_arithmetic_operators = {
            '<': increment_arithmetic_operators,
            '<=': increment_arithmetic_operators,
            '>': decrement_arithmetic_operators,
            '>=': decrement_arithmetic_operators,
            '==': '',
            '!=': ''
        }
        self.variables_bound_to_arithmetic_operators = {}

        self.boolean_expression = ''
        self.body = ''
        self.boolean_expression_and_body = ''
        self.for_cycle = ''
        self.condition = ''
        self.cycle = ''
        self.nested_operator = ''

        self.RANDOM_MIN_NUMBER = 1
        self.RANDOM_MAX_NUMBER = 100
        self.MIN_NUMBER_FOR_FOR_CYCLE = 1
        self.MAX_NUMBER_FOR_FOR_CYCLE = 10

    def remove_poorly_readable_variables(self):
        excluded_variables = ['i', 'l', 'o', 'O']
        for variable in excluded_variables:
            self.variables = self.variables.replace(variable, '')

    def generate_initialized_variables(self):
        self.count_variables = randint(2, 3)
        for i in range(self.count_variables):
            random_variable = choice(self.variables)
            self.initialized_variables[random_variable] = randint(1, 100)
            self.variables = self.variables.replace(random_variable, '')

    def get_random_number(self):
        return randint(self.RANDOM_MIN_NUMBER, self.RANDOM_MAX_NUMBER)

    def generate_code(self):
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
        self.generate_print_of_variable()
        return self.code

    def generate_variables(self):
        for key, value in self.initialized_variables.items():
            self.code += f'int {key} = {value};\n'

    def generate_nesting_of_operators(self):
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

    def generate_cycle(self):
        operator = choice(self.presence_one_of_cycles).title
        if operator == 'for':
            self.generate_for_with_body()
        else:
            self.generate_boolean_expression_and_body(operator)
            self.cycle = self.boolean_expression_and_body

    def generate_for_with_body(self):
        if self.cycle_condition == 'Составное':
            self.generate_compound_for_cycle()
            self.generate_body(is_random_variables=False)
        else:
            self.generate_simple_for_cycle()
            self.generate_body()
        self.cycle = self.for_cycle + self.body + '\n'
        if self.nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(self.nested_operator)
            self.cycle += nested_operator
        self.cycle += '}'

    def generate_body(self, is_random_variables=True):
        if is_random_variables:
            self.generate_body_with_random_variables()
        else:
            self.generate_body_with_variables_bound_to_arithmetic_operators()

    def generate_body_with_variables_bound_to_arithmetic_operators(self):
        self.body = ''
        i = 1
        for variable, arithmetic_operators in self.variables_bound_to_arithmetic_operators.items():
            if arithmetic_operators:
                random_arithmetic_operator = self.get_random_list_item(arithmetic_operators)
            else:
                random_arithmetic_operator = self.get_random_list_item(self.arithmetic_operators)
            self.body += f'\t{variable} {random_arithmetic_operator}= {self.get_random_number()};'
            is_last_variable = i != self.count_variables
            if is_last_variable:
                self.body += '\n'
            i += 1

    @staticmethod
    def get_random_list_item(roster):
        return choice(roster)

    def generate_body_with_random_variables(self):
        random_variable = self.get_random_dictionary_key(self.initialized_variables)
        random_arithmetic_operator = self.get_random_list_item(self.arithmetic_operators)
        self.body = f'\t{random_variable} {random_arithmetic_operator}= {self.get_random_number()};'

    def get_random_dictionary_key(self, dictionary):
        list_initialized_variables = self.get_list_dictionary_keys(dictionary)
        return choice(list_initialized_variables)

    @staticmethod
    def get_list_dictionary_keys(dictionary):
        return list(dictionary.keys())

    def generate_compound_for_cycle(self):
        random_variable = self.get_random_dictionary_key(self.initialized_variables)
        random_comparison_operator2 = self.get_random_comparison_operator()
        self.add_variable_bound_to_arithmetic_operator(random_variable, random_comparison_operator2)
        i = self.get_random_i()
        random_comparison_operator = self.get_random_dictionary_key(self.get_greater_and_less_comparison_operators())
        max_i = self.get_random_i()
        random_logical_operator = self.get_random_logical_operator()
        rand_int = self.get_random_number()
        arithmetic_operators = self.comparison_and_their_arithmetic_operators[random_comparison_operator]
        random_arithmetic_operator = self.get_random_list_item(arithmetic_operators)
        step = randint(1, 10)
        self.for_cycle = f'for (int i = {i}; i {random_comparison_operator} {max_i} {random_logical_operator} ' \
                         f'{random_variable} {random_comparison_operator2} {rand_int}; ' \
                         f'i {random_arithmetic_operator}= {step}) ' + '{\n'

    def get_greater_and_less_comparison_operators(self):
        greater_and_less_comparison_operators = self.comparison_and_their_arithmetic_operators.copy()
        del greater_and_less_comparison_operators['==']
        del greater_and_less_comparison_operators['!=']
        return greater_and_less_comparison_operators

    def get_random_logical_operator(self):
        return choice(self.logical_operators)

    def get_random_comparison_operator(self):
        return choice(self.comparison_operators)

    def generate_simple_for_cycle(self):
        i = self.get_random_number()
        max_i = self.get_random_number()
        step = self.get_random_number()
        random_comparison_operator = choice(['<', '<='])
        self.for_cycle = f'for (int i = {i}; i {random_comparison_operator} {max_i}; i += {step}) ' + '{\n'

    @staticmethod
    def add_tabs_to_paragraphs(text):
        return '\n'.join(f'\t{word}' for word in text.split('\n'))

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
                nested_operator = self.add_tabs_to_paragraphs(self.nested_operator)
                self.boolean_expression_and_body += '\n' + nested_operator
            self.boolean_expression_and_body += '\n}\n' + f'while {self.boolean_expression};'
        else:
            self.boolean_expression_and_body = operator + ' ' + self.boolean_expression + ' ' + '{\n' + self.body
            if self.nested_operator:
                nested_operator = self.add_tabs_to_paragraphs(self.nested_operator)
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
            greater_and_less_comparison_operators = self.get_greater_and_less_comparison_operators()
        for variable in self.initialized_variables.keys():
            if operator == 'if':
                random_comparison_operator = self.get_random_comparison_operator()
            else:
                random_comparison_operator = self.get_random_dictionary_key(greater_and_less_comparison_operators)
                self.add_arithmetic_operator_used(random_comparison_operator)
                self.add_variable_bound_to_arithmetic_operator(variable, random_comparison_operator)
            rand_int = self.get_random_number()
            logical_operator = self.get_random_logical_operator()
            variable_comparison = f'{variable} {random_comparison_operator} {rand_int}'
            if i == self.count_variables:
                self.boolean_expression = f'(' + self.boolean_expression + f'{variable_comparison})'
            else:
                self.boolean_expression += f'{variable_comparison} {logical_operator} '
            i += 1

    def generate_simple_boolean_expression(self, operator):
        random_variable = self.get_random_dictionary_key(self.initialized_variables)
        rand_int = self.get_random_number()
        if operator == 'if':
            random_comparison_operator = self.get_random_comparison_operator()
        else:
            greater_and_less_comparison_operators = self.get_greater_and_less_comparison_operators()
            random_comparison_operator = self.get_random_dictionary_key(greater_and_less_comparison_operators)
            self.add_arithmetic_operator_used(random_comparison_operator)
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
        self.code += f'\nSystem.out.println("{random_variable} = " + {random_variable});'

    def add_arithmetic_operator_used(self, comparison_operator):
        self.arithmetic_operators_used += self.comparison_and_their_arithmetic_operators[
            comparison_operator]

    def add_variable_bound_to_arithmetic_operator(self, variable, comparison_operator):
        self.variables_bound_to_arithmetic_operators[variable] = self.comparison_and_their_arithmetic_operators[
            comparison_operator]

    @staticmethod
    def get_random_i():
        return randint(0, 10)
