import string
from random import randint, choice

from testing.services.code_conversion import JavaToPythonConversion


class RandomizerJava:
    def __init__(self):
        self.code = ''

        self.condition = 'if'
        self.condition_of_if_operator = 'Составное'
        self.cycle = 'while'
        self.cycle_condition = 'Составное'
        self.operator_nesting = 'оператор if вложен в '

        self.variables = self.remove_poorly_readable_variables()
        self.comparison_operators = ['<', '<=', '>', '>=', '==', '!=']
        self.logical_operators = ['&&', '||']
        self.arithmetic_operators = ['+', '-', '*', '/']
        count_variables = randint(2, 3)
        # баг с 1 переменной
        self.initialized_variables = {choice(self.variables): randint(0, 100) for i in
                                      range(count_variables)}
        self.generate_code()
        print(self.code)
        # JavaToPythonConversion(self.code)

    @staticmethod
    def remove_poorly_readable_variables():
        excluded_variables = ['i', 'l', 'o', 'O']
        variables = string.ascii_letters
        for variable in excluded_variables:
            variables = variables.replace(variable, '')
        return variables

    def generate_code(self):
        # Формирование переменных
        self.generate_variables()
        # Вложенность операторов
        operator_nesting = 1
        # Наличие оператора if
        is_if_operator = 1
        # наличие одного из следующих циклов
        is_presence_of_cycles = 1
        if operator_nesting:
            self.code += self.get_nesting_of_operators()
        elif is_if_operator and is_presence_of_cycles:
            self.code += self.get_condition_and_loop()
        elif is_if_operator:
            self.code += self.get_generated_condition()
        elif is_presence_of_cycles:
            self.code += self.get_generated_cycle()
        self.code += '\n' + self.get_print_of_variable()

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
        computing_process = self.condition
        if self.condition_of_if_operator == 'Составное':
            return self.get_compound_boolean_expression_with_body(computing_process, nested_operator)
        else:
            return self.get_simple_boolean_expression_with_body(computing_process, nested_operator)

    def get_compound_boolean_expression(self):
        """Сгенерирует составное логическое выражение"""
        boolean_expression = ''
        i = 1
        for variable in self.initialized_variables.keys():
            comparison_operator = self.get_random_comparison_operator()
            rand_int = randint(0, 100)
            logical_operator = self.get_random_logical_operator()
            variable_comparison = f'{variable} {comparison_operator} {rand_int}'
            count_variables = len(self.initialized_variables)
            if i == count_variables:
                boolean_expression = f'(' + boolean_expression + f'{variable_comparison})'
            else:
                boolean_expression += f'{variable_comparison} {logical_operator} '
            i += 1
        return boolean_expression

    def get_generated_cycle(self, nested_operator=''):
        """Сгенерирует цикл"""
        computing_process = self.cycle
        if self.cycle_condition == 'Составное':
            if computing_process == 'for':
                pass
            elif computing_process == 'do-while':
                boolean_expression = self.get_compound_boolean_expression()
                return self.get_do_while_loop(boolean_expression, nested_operator)
            else:
                return self.get_compound_boolean_expression_with_body(computing_process, nested_operator)
        else:
            if computing_process == 'for':
                return self.get_simple_for_with_body(nested_operator)
            elif computing_process == 'do-while':
                boolean_expression = self.get_simple_boolean_expression()
                return self.get_do_while_loop(boolean_expression, nested_operator)
            else:
                return self.get_simple_boolean_expression_with_body(computing_process, nested_operator)

    def get_do_while_loop(self, boolean_expression, nested_operator):
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            return 'do {\n' + self.get_generated_body() + '\n' + nested_operator + '\n}\n' \
                + f'while {boolean_expression};'
        return 'do {\n' + self.get_generated_body() + '\n}\n' + f'while {boolean_expression};'

    def get_compound_boolean_expression_with_body(self, computing_process, nested_operator):
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            return computing_process + ' ' + self.get_compound_boolean_expression() + ' ' + '{\n' \
                + self.get_generated_body() + '\n' + nested_operator + '\n}'
        return computing_process + ' ' + self.get_compound_boolean_expression() + ' ' + '{\n' \
            + self.get_generated_body() + '\n}'

    def get_simple_boolean_expression_with_body(self, computing_process, nested_operator):
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            return computing_process + ' ' + self.get_simple_boolean_expression() + ' {\n' \
                + self.get_generated_body() + '\n' + nested_operator + '\n}'
        return computing_process + ' ' + self.get_simple_boolean_expression() + ' {\n' + \
            self.get_generated_body() + '\n}'

    def get_boolean_expression_with_body(self, computing_process, nested_operator, condition):
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            return computing_process + ' ' + self.get_compound_boolean_expression() + ' ' + '{\n' \
                + self.get_generated_body() + '\n' + nested_operator + '\n}'
        return computing_process + ' ' + self.get_compound_boolean_expression() + ' ' + '{\n' \
            + self.get_generated_body() + '\n}'

    def get_print_of_variable(self):
        list_variables = list(self.initialized_variables)
        random_variable = choice(list_variables)
        # return f'print("{random_variable} =", {random_variable})'
        return f'System.out.printIn("{random_variable} = " + {random_variable});'

    @staticmethod
    def add_tabs_to_paragraphs(text):
        return '\n'.join(f'\t{word}' for word in text.split('\n'))

    def get_simple_for_with_body(self, nested_operator):
        body_for = self.get_simple_for() + self.get_generated_body()
        if nested_operator:
            nested_operator = self.add_tabs_to_paragraphs(nested_operator)
            return body_for + '\n' + nested_operator + '\n}'
        return body_for + '\n}'

    @staticmethod
    def get_simple_for():
        min_number = 1
        max_number = 10
        i = randint(min_number, max_number)
        max_i = randint(min_number, max_number)
        step = randint(min_number, max_number)
        random_comparison_operator = choice(['<', '<='])
        return f'for (int i = {i}; i {random_comparison_operator} {max_i}; i += {step}) ' + '{\n'

    def get_generated_body(self):
        """Сгенерирует тело"""
        variable = self.get_random_initialized_variable()
        arithmetic_operator = self.get_random_arithmetic_operator()
        rand_int = randint(0, 100)
        return f'\t{variable} {arithmetic_operator}= {rand_int};'

    def get_random_comparison_operator(self):
        return choice(self.comparison_operators)

    def get_random_logical_operator(self):
        return choice(self.logical_operators)

    def get_list_initialized_variables(self):
        return list(self.initialized_variables.keys())

    def get_simple_boolean_expression(self):
        variable = self.get_random_initialized_variable()
        comparison_operator = self.get_random_comparison_operator()
        rand_int = randint(0, 100)
        return f'({variable} {comparison_operator} {rand_int})'

    def get_random_initialized_variable(self):
        list_initialized_variables = self.get_list_initialized_variables()
        return choice(list_initialized_variables)

    def get_random_arithmetic_operator(self):
        return choice(self.arithmetic_operators)


if __name__ == '__main__':
    RandomizerJava()
