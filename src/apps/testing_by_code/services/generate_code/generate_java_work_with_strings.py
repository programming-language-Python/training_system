from random import choice

from apps.testing_by_code.abstractions import Variable
from apps.testing_by_code.services.generate_code.templates import get_string_template, \
    get_string_template_without_body
from apps.testing_by_code.utils.random_value import get_N_digits, get_digit, \
    get_number_in_range
from apps.testing_by_code.utils.utils import remove_empty_paragraphs


class GenerateJavaWorkWithStrings:
    variable_1: str
    variable_2: str

    def __init__(self):
        variable = Variable()
        self.variable_1 = variable.get_random()
        self.variable_2 = variable.get_random()

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
        string = self.get_string(
            value=get_N_digits(quantity_digit=6)
        )
        find = get_digit()
        replace = get_digit()
        body = f'String {self.variable_2} = {self.variable_1}' \
               f'.replace("{find}", "{replace}");'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def get_string(self, value: int) -> str:
        return f'String {self.variable_1} = "{value}";'

    def generate_compare_to(self) -> str:
        string = self.get_string(value=get_N_digits(quantity_digit=6))
        body = f'String {self.variable_2} = "{get_N_digits(quantity_digit=6)}";'
        print_ = f'{self.variable_1}.compareTo({self.variable_2})'
        return get_string_template(string, body, print_)

    def generate_length(self) -> str:
        string = self.get_string(value=get_N_digits())
        body = f'int {self.variable_2} = {self.variable_1}.length();'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_char_at(self) -> str:
        value = get_N_digits()
        string = self.get_string(value)
        max_index = len(str(value)) - 1
        random_digit = get_number_in_range(end=max_index)
        print_ = f'{self.variable_1}.charAt({random_digit})'
        return get_string_template_without_body(string, print_)

    def generate_substring(self) -> str:
        value = get_N_digits()
        string = self.get_string(value)
        max_index = len(str(value)) - 1
        argument = get_digit(max_digit=max_index)
        body = f'String {self.variable_2} = {self.variable_1}' \
               f'.substring({argument});'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_index_of(self) -> str:
        string = self.get_string(value=get_N_digits(quantity_digit=6))
        argument = get_digit()
        body = f'int {self.variable_2} = {self.variable_1}' \
               f'.indexOf("{argument}");'
        print_ = self.variable_2
        return get_string_template(string, body, print_)

    def generate_last_index_of(self) -> str:
        string = self.get_string(value=get_N_digits(quantity_digit=6))
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
