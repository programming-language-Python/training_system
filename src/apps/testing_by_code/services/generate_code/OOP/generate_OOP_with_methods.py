from random import choice

from apps.testing_by_code import abstractions
from apps.testing_by_code.services.generate_code.config import ARITHMETIC_OPERATORS, NUMERIC_DATA_TYPES
from apps.testing_by_code.interfaces import IOop
from apps.testing_by_code.services.generate_code.templates import get_print_template
from apps.testing_by_code.utils.random_value import get_number, get_int


class GenerateOOPWithMethods(abstractions.OOP, IOop):
    numeric_data_type: str
    method_1: str
    method_2: str
    class_example_variable: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numeric_data_type = choice(NUMERIC_DATA_TYPES)
        self.method_1 = self.get_random()
        self.method_2 = self.get_random()
        self.class_example_variable = self.get_random()

    def _generate_class_example_body(self):
        class_example_body = f'''
    {self.numeric_data_type} {self.variable};
    Example({self.numeric_data_type} {self.variable}){'{'}
        this.{self.variable} = {self.variable};
    {'}'}
    void {self.method_1}({self.numeric_data_type} {self.variable}){'{'}
        {self.variable} {choice(ARITHMETIC_OPERATORS)}= {self._get_number()};
    {'}'}
    void {self.method_2}(Example {self.class_example_variable}){'{'}
        {self.class_example_variable}.{self.variable} {choice(ARITHMETIC_OPERATORS)}= {self._get_number()};
    {'}'}'''
        return class_example_body

    def _get_number(self) -> str:
        is_float_data_type = 'float' in self.numeric_data_type
        if is_float_data_type:
            return f'{get_number()}f'

        is_double_data_type = 'double' in self.numeric_data_type
        if is_double_data_type:
            return f'{get_number()}'

        return f'{get_int()}'

    def _generate_class_main_body(self) -> str:
        argument = choice([self.variable, self.class_example_variable])
        class_example_name = ''
        if argument == self.class_example_variable:
            class_example_name = f'''{self.class_example_variable}.'''
        method = self.method_1 if argument == self.variable else self.method_2
        print_ = f'{class_example_name}{self.variable}'
        class_main_body = f'''
    {self.numeric_data_type} {self.variable} = {self._get_number()};
    Example {self.class_example_variable} = new Example({self.variable});
    {self.class_example_variable}.{method}({argument});
    {get_print_template(text=print_)}'''
        return class_main_body


if __name__ == '__main__':
    test = GenerateOOPWithMethods()
    print(test.execute())
