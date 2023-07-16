from random import choice

from testing.services.generate_code.abstractions import Variable
from testing.services.generate_code.templates import get_string_template, \
    get_string_template_without_body
from testing.utils.random_value import get_N_digits, get_digit, \
    get_number_in_range
from testing.utils.utils import remove_empty_paragraphs


class GenerateJavaWorkWithStrings:
    variable_1: str
    variable_2: str
    number: int

    def __init__(self):
        variable = Variable()
        self.variable_1 = variable.get_random()
        self.variable_2 = variable.get_random()
        self.number = get_N_digits()

    def execute(self):
        methods = [
            self.generate_replace,
            self.generate_compare_to,
            self.generate_length,
            self.generate_char_at,
            self.generate_substring,
            self.generate_index_of,
            self.generate_last_index_of,
            self.generate_concatenation,
        ]
        code = choice(methods)()
        return remove_empty_paragraphs(code)

    def generate_replace(self) -> str:
        string = self.get_string()
        find = get_digit()
        replace = get_digit()
        body = f'String {self.variable_2} = {self.variable_1}' \
               f'.replace("{find}", "{replace}");'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def get_string(self) -> str:
        return f'String {self.variable_1} = "{self.number}";'

    def generate_compare_to(self) -> str:
        string = self.get_string()
        body = f'String {self.variable_2} = "{get_N_digits()}";'
        print_ = f'{self.variable_1}.compareTo({self.variable_2})'
        return get_string_template(string, body, print_)

    def generate_length(self) -> str:
        string = self.get_string()
        body = f'int {self.variable_2} = {self.variable_1}.length();'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_char_at(self) -> str:
        string = self.get_string()
        max_index = len(str(self.number)) - 1
        random_digit = get_number_in_range(end=max_index)
        print_ = f'{self.variable_1}.charAt({random_digit})'
        return get_string_template_without_body(string, print_)

    def generate_substring(self) -> str:
        string = self.get_string()
        argument = get_digit()
        body = f'String {self.variable_2} = {self.variable_1}' \
               f'.substring({argument});'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_index_of(self) -> str:
        string = self.get_string()
        argument = get_digit()
        body = f'int {self.variable_2} = {self.variable_1}' \
               f'.indexOf("{argument}");'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_last_index_of(self) -> str:
        string = self.get_string()
        argument = get_digit()
        body = f'int {self.variable_2} = {self.variable_1}' \
               f'.lastIndexOf("{argument}");'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_concatenation(self) -> str:
        digit_1 = get_digit()
        digit_2 = get_digit()
        string = f'String {self.variable_1} = "x=" + {digit_1} + {digit_2};'
        print_ = self.variable_1
        return get_string_template_without_body(string, print_)


if __name__ == '__main__':
    GenerateJavaString = GenerateJavaWorkWithStrings()
    print(GenerateJavaString.execute())
