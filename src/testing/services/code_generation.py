import string
from random import randint, choice


class RandomizerJava:
    def __init__(self, **task_setup):
        self.code = ''

        self.use_of_all_variables = task_setup['use_of_all_variables']
        self.is_if_operator = task_setup['is_if_operator'] == 'Присутствует'
        self.condition_of_if_operator = task_setup['condition_of_if_operator']
        self.presence_one_of_cycles = task_setup['presence_one_of_cycles']
        self.cycle_condition = task_setup['cycle_condition']
        self.operator_nesting = task_setup['operator_nesting']

        # self.is_if_operator = True
        # self.condition_of_if_operator = 'Составное'
        # self.presence_one_of_cycles = ['while', 'do-while']
        # self.cycle_condition = 'Составное'
        # self.operator_nesting = 'оператор if вложен в цикл'

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

        # print(self.generate_code())
        # JavaToPythonConversion(self.code)

    def generate_initialized_variables(self):
        self.count_variables = randint(2, 3)
        # баг с 1 переменной
        for i in range(self.count_variables):
            random_variable = choice(self.variables)
            self.initialized_variables[random_variable] = randint(0, 100)
            self.variables = self.variables.replace(random_variable, '')

    def remove_poorly_readable_variables(self):
        excluded_variables = ['i', 'l', 'o', 'O']
        for variable in excluded_variables:
            self.variables = self.variables.replace(variable, '')

    def generate_code(self):
        # Формирование переменных
        self.generate_variables()
        if self.operator_nesting:
            self.code += self.get_nesting_of_operators()
        elif self.is_if_operator and self.presence_one_of_cycles:
            self.code += self.get_condition_and_loop()
        elif self.is_if_operator:
            self.code += self.get_generated_condition()
        elif self.presence_one_of_cycles:
            self.code += self.get_generated_cycle()
        self.code += '\n' + self.get_print_of_variable()
        print(self.code)
        return self.code

    def get_condition_and_loop(self):
        condition = self.get_generated_condition()
        cycle = self.get_generated_cycle()
        condition_and_cycle = [condition, cycle]
        random_index = randint(0, 1)
        return condition_and_cycle.pop(random_index) + '\n' + condition_and_cycle[0]

    def generate_variables(self):
        for key, value in self.initialized_variables.items():
            self.code += f'int {key} = {value};\n'

    def get_nesting_of_operators(self):
        """
        оператор if вложен в цикл
        цикл вложен в оператор if
        """
        if self.operator_nesting == 'оператор if вложен в цикл':
            cycle = self.get_generated_cycle()
            nested_operator = self.get_generated_condition(cycle)
        else:
            condition = self.get_generated_condition()
            nested_operator = self.get_generated_cycle(condition)
        return nested_operator

    def get_generated_condition(self, nested_operator=''):
        """Сгенерирует условие"""
        operator = 'if'
        condition = self.condition_of_if_operator
        return self.get_boolean_expression_with_body(operator,
                                                     condition,
                                                     nested_operator)

    def generate_compound_boolean_expression(self, operator):
        """Сгенерирует составное логическое выражение"""
        self.boolean_expression = ''
        i = 1
        is_while_or_do_while_loop = operator == 'while' or operator == 'do-while'
        if is_while_or_do_while_loop:
            comparison_and_their_arithmetic_operators = self.comparison_and_their_arithmetic_operators.copy()
            del comparison_and_their_arithmetic_operators['==']
            del comparison_and_their_arithmetic_operators['!=']
        for variable in self.initialized_variables.keys():
            if is_while_or_do_while_loop:
                random_comparison_operator = self.get_random_dictionary_key(
                    comparison_and_their_arithmetic_operators)
                self.add_arithmetic_operators_used(random_comparison_operator)
                self.variables_bound_to_arithmetic_operators[variable] = self.comparison_and_their_arithmetic_operators[
                    random_comparison_operator]
            else:
                random_comparison_operator = self.get_random_comparison_operator()
            rand_int = randint(0, 100)
            logical_operator = self.get_random_logical_operator()
            variable_comparison = f'{variable} {random_comparison_operator} {rand_int}'
            if i == self.count_variables:
                self.boolean_expression = f'(' + self.boolean_expression + f'{variable_comparison})'
            else:
                self.boolean_expression += f'{variable_comparison} {logical_operator} '
            i += 1

    def add_arithmetic_operators_used(self, comparison_operator):
        self.arithmetic_operators_used += self.comparison_and_their_arithmetic_operators[
            comparison_operator]

    def get_generated_cycle(self, nested_operator=''):
        """Сгенерирует цикл"""
        operator = choice(self.presence_one_of_cycles).title
        if operator == 'for':
            return self.get_for_with_body(nested_operator)
        elif operator == 'while':
            condition = self.cycle_condition
            return self.get_boolean_expression_with_body(operator, condition, nested_operator)
        elif operator == 'do-while':
            return self.get_do_while_loop(nested_operator)

    def get_for_with_body(self, nested_operator):
        if self.cycle_condition == 'Составное':
            pass
        else:
            self.generate_body()
            body_for = self.get_simple_for() + self.body
            if nested_operator:
                nested_operator = self.add_tabs_to_paragraphs(nested_operator)
                return body_for + '\n' + nested_operator + '\n}'
        return body_for + '\n}'

    def get_boolean_expression_with_body(self, operator, condition, nested_operator):
        self.generate_boolean_expression(operator, condition)
        if operator == 'while':
            self.generate_body(is_while_loop=True)
            start_of_boolean_expression = operator + ' ' + self.boolean_expression + ' ' + '{\n' + self.body
        else:
            self.generate_body()
            start_of_boolean_expression = operator + ' ' + self.boolean_expression + ' ' + '{\n' + self.body
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            start_of_boolean_expression += '\n' + nested_operator
        return start_of_boolean_expression + '\n}'

    def get_do_while_loop(self, nested_operator):
        self.generate_boolean_expression('do-while', self.cycle_condition)
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            self.generate_body(is_while_loop=True)
            return 'do {\n' + self.body + '\n' + nested_operator + '\n}\n' \
                + f'while {self.boolean_expression};'
        return 'do {\n' + self.body + '\n}\n' + f'while {self.boolean_expression};'

    def get_print_of_variable(self):
        list_variables = list(self.initialized_variables)
        random_variable = choice(list_variables)
        # return f'print("{random_variable} =", {random_variable})'
        return f'System.out.println("{random_variable} = " + {random_variable});'

    @staticmethod
    def add_tabs_to_paragraphs(text):
        return '\n'.join(f'\t{word}' for word in text.split('\n'))

    @staticmethod
    def get_simple_for():
        min_number = 1
        max_number = 10
        i = randint(min_number, max_number)
        max_i = randint(min_number, max_number)
        step = randint(min_number, max_number)
        random_comparison_operator = choice(['<', '<='])
        return f'for (int i = {i}; i {random_comparison_operator} {max_i}; i += {step}) ' + '{\n'

    def generate_body(self, is_while_loop=False):
        """Сгенерирует тело"""
        self.body = ''
        if is_while_loop:
            self.generate_body_of_while_or_do_while_loop()
        else:
            random_variable = self.get_random_dictionary_key(self.initialized_variables)
            random_arithmetic_operator = self.get_random_list_item(self.arithmetic_operators)
            self.body = f'\t{random_variable} {random_arithmetic_operator}= {randint(0, 100)};'

    def generate_body_of_while_or_do_while_loop(self):
        for variable, arithmetic_operators in self.variables_bound_to_arithmetic_operators.items():
            if arithmetic_operators:
                random_arithmetic_operator = self.get_random_list_item(arithmetic_operators)
            else:
                random_arithmetic_operator = self.get_random_list_item(self.arithmetic_operators)
            self.body += f'\t{variable} {random_arithmetic_operator}= {randint(0, 100)};\n'

    def generate_boolean_expression(self, operator, condition):
        if condition == 'Составное':
            self.generate_compound_boolean_expression(operator)
            return
        return self.get_simple_boolean_expression()

    def get_random_comparison_operator(self):
        return choice(self.comparison_operators)

    def get_random_logical_operator(self):
        return choice(self.logical_operators)

    def get_simple_boolean_expression(self):
        random_variable = self.get_random_dictionary_key(self.initialized_variables)
        comparison_operator = self.get_random_comparison_operator()
        rand_int = randint(0, 100)
        return f'({random_variable} {comparison_operator} {rand_int})'

    def get_random_dictionary_key(self, dictionary):
        list_initialized_variables = self.get_list_dictionary_keys(dictionary)
        return choice(list_initialized_variables)

    @staticmethod
    def get_list_dictionary_keys(dictionary):
        return list(dictionary.keys())

    @staticmethod
    def get_random_list_item(roster):
        return choice(roster)


if __name__ == '__main__':
    RandomizerJava()
