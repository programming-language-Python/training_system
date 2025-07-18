from random import choice

from apps.testing_by_code import abstractions
from apps.testing_by_code.services.generate_code.config import INTEGER_DATA_TYPES
from apps.testing_by_code.interfaces import IOop
from apps.testing_by_code.services.generate_code.templates import get_print_template
from apps.testing_by_code.utils.random_value import get_int


class GenerateOOPWithReturn(abstractions.OOP, IOop):
    variable_type_1: str
    variable_type_2: str
    variable: str
    method_type: str
    method: str
    class_example_variable: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        integer_data_types = INTEGER_DATA_TYPES.copy()
        variable_type_1 = choice(integer_data_types)
        integer_data_types.remove(variable_type_1)
        self.variable_type_1 = variable_type_1
        self.variable_type_2 = choice(integer_data_types)
        self.variable = self.get_random()
        self.method_type = choice(INTEGER_DATA_TYPES)
        self.method = self.get_random()
        self.class_example_variable = self.get_random()

    def _generate_class_example_body(self) -> str:
        class_example_body_with_return = f'''
    {self.method_type} {self.method}(){'{'}
        return {get_int()};
    {'}'}
    {self.method_type} {self.method}({self.variable_type_1} {self.variable}){'{'}
        return {get_int()};
    {'}'}
    {self.method_type} {self.method}({self.variable_type_2} {self.variable}){'{'}
        return {get_int()};
    {'}'}'''
        return class_example_body_with_return

    def _generate_class_main_body(self) -> str:
        variable_type = choice([self.variable_type_1, self.variable_type_2])
        variables = [self.get_random(), '']
        variable_2 = choice(variables)
        initialized_variable = ''
        is_variable_2 = variable_2 != ''
        if is_variable_2:
            initialized_variable = f'''{variable_type} {variable_2} = {get_int()};'''
        class_main_body_with_return = f'''
    Example {self.class_example_variable} = new Example();
    {initialized_variable}
    {self.method_type} {self.variable} = {self.class_example_variable}.{self.method}({variable_2});
    {get_print_template(text=self.variable)}'''
        return class_main_body_with_return
