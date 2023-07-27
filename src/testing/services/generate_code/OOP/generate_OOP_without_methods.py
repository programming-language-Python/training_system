from random import choice

from testing import abstractions
from testing.services.generate_code.config import INTEGER_DATA_TYPES
from testing.interfaces import IOop
from testing.services.generate_code.templates import get_print_template
from testing.utils.random_value import get_int


class GenerateOOPWithoutMethods(abstractions.OOP, IOop):
    int_data_type: str
    variable: str
    class_example_variable: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.int_data_type = choice(INTEGER_DATA_TYPES)
        self.variable = self.get_random()
        self.class_example_variable = self.get_random()

    def _generate_class_example_body(self) -> str:
        return f'''{self.int_data_type} {self.variable};'''

    def _generate_class_main_body(self) -> str:
        class_example_variable_2 = self.get_random()
        print_ = f'{self.class_example_variable}.{self.variable} + " "' \
                 f' + {class_example_variable_2}.{self.variable}'
        class_main_without_methods = f'''
    Example {self.class_example_variable} = new Example();
    Example {class_example_variable_2} = {self.class_example_variable};
    {self.class_example_variable}.{self.variable} = {get_int()};
    {class_example_variable_2}.{self.variable} = {get_int()};
    {get_print_template(text=print_)}'''
        return class_main_without_methods


if __name__ == '__main__':
    generate_oop_without_methods = GenerateOOPWithoutMethods()
    print(generate_oop_without_methods.execute())
