import string
from random import randint, choice


class CodeRandomizer:
    def __init__(self):
        self.variables = self.remove_poorly_readable_variables()
        self.comparison_operators = ['<', '<=', '>', '>=', '==', '!=']
        self.logical_operators = ['and', 'or']
        self.arithmetic_operators = ['+', '-', '*', '/']
        self.number_of_variables = randint(2, 3)
        self.initialized_variables = {choice(self.variables): randint(0, 100) for i in
                                      range(self.number_of_variables)}
        self.code = ''

        self.generate_code()
        print(self.code)

    @staticmethod
    def remove_poorly_readable_variables():
        hard_to_read_variables = ['l', 'o', 'O']
        variables = string.ascii_letters
        for variable in hard_to_read_variables:
            variables = variables.replace(variable, '')
        return variables

    def generate_code(self):
        # Формирование переменных
        for key, value in self.initialized_variables.items():
            self.code += f'{key} = {value}\n'

        # Наличие оператора if
        is_if_operator = 1
        if is_if_operator:
            self.get_generated_condition()

        # наличие одного из следующих циклов
        is_presence_of_cycles = 1
        if is_presence_of_cycles:
            print(self.get_generated_cycle())

        # Вложенность операторов
        # operator_nesting = 1
        # if operator_nesting:
        #     сгенерировать вложенность операторов

    def get_generated_condition(self):
        """Сгенерирует условие"""
        computing_process = 'if'
        condition_of_if_operator = 'Составное'
        if condition_of_if_operator == 'Составное':
            return self.get_compound_boolean_expression(computing_process)
        else:
            return self.get_simple_boolean_expression(computing_process)

    def get_generated_cycle(self):
        """Сгенерирует цикл"""
        computing_process = 'while'
        # if computing_process == 'for':
        #     получить

        cycle_condition = 'Составное'
        if cycle_condition == 'Составное':
            return self.get_compound_boolean_expression(computing_process)
        else:
            return self.get_simple_boolean_expression(computing_process)

    def get_compound_boolean_expression(self, computing_process):
        """Сгенерирует составное логическое выражение"""
        boolean_expression = ''
        i = 1
        for variable in self.initialized_variables.keys():
            comparison_operator = self.get_random_comparison_operator()
            rand_int = randint(0, 100)
            logical_operator = self.get_random_logical_operator()
            variable_comparison = f'{variable} {comparison_operator} {rand_int}'
            if i == self.number_of_variables:
                boolean_expression = f'{computing_process} ' + boolean_expression + f'{variable_comparison}:\n'
            else:
                boolean_expression += f'{variable_comparison} {logical_operator} '
            i += 1
        return boolean_expression + self.get_generated_body()

    def get_random_comparison_operator(self):
        return choice(self.comparison_operators)

    def get_random_logical_operator(self):
        return choice(self.logical_operators)

    def get_simple_boolean_expression(self, computing_process):
        variable = self.get_random_initialized_variable()
        comparison_operator = self.get_random_comparison_operator()
        rand_int = randint(0, 100)
        return f'{computing_process} {variable} {comparison_operator} {rand_int}:\n' + self.get_generated_body()

    def get_random_initialized_variable(self):
        list_initialized_variables = self.get_list_initialized_variables()
        return choice(list_initialized_variables)

    def get_list_initialized_variables(self):
        return list(self.initialized_variables.keys())

    def get_generated_body(self):
        """Сгенерирует тело"""
        variable = self.get_random_initialized_variable()
        arithmetic_operator = self.get_random_arithmetic_operator()
        rand_int = randint(0, 100)
        return f'\t{variable} {arithmetic_operator}= {rand_int}\n'

    def get_random_arithmetic_operator(self):
        return choice(self.arithmetic_operators)


if __name__ == '__main__':
    CodeRandomizer()
