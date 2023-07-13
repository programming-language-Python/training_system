# from random import choice
#
# from testing.services.generate_code.config import NUMERIC_DATA_TYPES, INTEGER_DATA_TYPES, REAL_DATA_TYPES
# from testing.utils import random_value
# from testing.utils.utils import remove_empty_paragraphs, add_tabs
#
#
# class GenerateJavaOOP:
#     variables: str = None
#     numeric_data_type: str = None
#     int_data_type: str = None
#     real_data_type: str = None
#     method_type: str = None
#     variable_type_1: str = None
#     variable_type_2: str = None
#     variable: str = None
#     method_1: str = None
#     method_2: str = None
#     class_example_random_variable: str = None
#     codes: list = None
#     suffix: str = ''
#
#     def __init__(self) -> None:
#         self.variables = _get_readable_variables()
#         self.numeric_data_type = choice(NUMERIC_DATA_TYPES)
#         self.int_data_type = choice(INTEGER_DATA_TYPES)
#         self.real_data_type = choice(REAL_DATA_TYPES)
#         self.method_type = choice(INTEGER_DATA_TYPES)
#         self.variable_type_1 = choice(INTEGER_DATA_TYPES)
#         self.variable_type_2 = choice(INTEGER_DATA_TYPES)
#         self.variable = self.get_random_variable()
#         self.method_1 = self.get_random_variable()
#         self.method_2 = self.get_random_variable()
#         self.class_example_random_variable = self.get_random_variable()
#         self.codes = [
#             self.get_code_with_methods(),
#             self.get_code_with_return(),
#             self.get_code_with_int_and_without_methods()
#         ]
#
#     def get_random_variable(self) -> str:
#         variable = choice(self.variables)
#         self.variables = self.variables.replace(variable, '')
#         return variable
#
#     def execute(self) -> str:
#         random_code = choice(self.codes)
#         return remove_empty_paragraphs(random_code)
#
#     def get_code_with_methods(self):
#         is_integer_data_type = any(map(lambda v: v in self.numeric_data_type, Config.INTEGER_DATA_TYPES))
#         if is_integer_data_type:
#             return self.get_code_with_int()
#         return self.get_code_with_float()
#
#     def get_code_with_int(self) -> str:
#         return self.generate_class_example_with_int_type() + self.generate_class_main_with_int_type()
#
#     def generate_class_example_with_int_type(self) -> str:
#         declared_variable = f'''{self.numeric_data_type} {self.variable};'''
#         class_example_body_with_int_type = declared_variable + f'''
#     Example({self.numeric_data_type} {self.variable}){'{'}
#         this.{self.variable} = {self.variable};
#     {'}'}
#     void {self.method_1}({self.numeric_data_type} {self.variable}){'{'}
#         {self.variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_int()};
#     {'}'}
#     void {self.method_2}(Example {self.class_example_random_variable}){'{'}
#         {self.class_example_random_variable}.{self.variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_int()};
#     {'}'}'''
#         return self.get_class_example(class_example_body_with_int_type)
#
#     @staticmethod
#     def get_class_example(body: str) -> str:
#         return f'''
# class Example {'{'}
#     {body}
# {'}'}'''
#
#     def generate_class_main_with_int_type(self) -> str:
#         random_argument = choice([self.variable, self.class_example_random_variable])
#         random_method = self.method_1 if random_argument == self.variable else self.method_2
#         class_example_name = ''
#         if random_argument == self.class_example_random_variable:
#             class_example_name = f'''{self.class_example_random_variable}.'''
#
#         class_main_body_with_int_type = f'''
#     {self.numeric_data_type} {self.variable} = {self.random_value.get_int()};
#     Example {self.class_example_random_variable} = new Example({self.variable});
#     {self.class_example_random_variable}.{random_method}({random_argument});
#     System.out.println({class_example_name}{self.variable});'''
#         return self.get_class_main(class_main_body_with_int_type)
#
#     @staticmethod
#     def get_class_main(body: str) -> str:
#         return f'''
# public class Main {'{'}
#     public static void main(String[] args) {'{'}
#         {add_tabs(body)}
#     {'}'}
# {'}'}'''
#
#     def get_code_with_float(self) -> str:
#         is_float_data_type = 'float' in self.numeric_data_type
#         if is_float_data_type:
#             self.suffix = 'f'
#         return self.generate_class_example_body_with_float_type() + self.generate_class_main_body_with_float_type()
#
#     def generate_class_example_body_with_float_type(self) -> str:
#         class_example_body_with_float_type = f'''
#     {self.numeric_data_type} {self.variable};
#     Example({self.numeric_data_type} {self.variable}){'{'}
#         this.{self.variable} = {self.variable};
#     {'}'}
#     void {self.method_1}({self.numeric_data_type} {self.variable}){'{'}
#         {self.variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_number()}{self.suffix};
#     {'}'}
#     void {self.method_2}(Example {self.class_example_random_variable}){'{'}
#         {self.class_example_random_variable}.{self.variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_number()}{self.suffix};
#     {'}'}'''
#         return self.get_class_example(class_example_body_with_float_type)
#
#     def generate_class_main_body_with_float_type(self):
#         class_main_body_with_float_type = f'''
#     {self.numeric_data_type} {self.variable} = {self.random_value.get_number()}{self.suffix};
#     Example {self.class_example_random_variable} = new Example({self.variable});
#     {self.class_example_random_variable}.{self.method_1}({self.variable});
#     System.out.println({self.variable});'''
#         return self.get_class_main(class_main_body_with_float_type)
#
#     def get_code_with_return(self) -> str:
#         return self.generate_class_example_with_return() + self.generate_class_main_with_return()
#
#     def generate_class_example_with_return(self) -> str:
#         class_example_body_with_return = f'''
#     {self.method_type} {self.method_1}(){'{'}
#         return {self.random_value.get_int()};
#     {'}'}
#     {self.method_type} {self.method_1}({self.variable_type_1} {self.variable}){'{'}
#         return {self.random_value.get_int()};
#     {'}'}
#     {self.method_type} {self.method_1}({self.variable_type_2} {self.variable}){'{'}
#         return {self.random_value.get_int()};
#     {'}'}'''
#         return self.get_class_example(class_example_body_with_return)
#
#     def generate_class_main_with_return(self) -> str:
#         random_variable_type = choice([self.variable_type_1, self.variable_type_2])
#         variables = [self.get_random_variable(), '']
#         random_variable_2 = choice(variables)
#         initialized_variable = ''
#         is_variable_2 = random_variable_2 != ''
#         if is_variable_2:
#             initialized_variable = f'''{random_variable_type} {random_variable_2} = {self.random_value.get_int()};'''
#         class_main_body_with_return = f'''
#     Example {self.class_example_random_variable} = new Example();
#     {initialized_variable}
#     {self.method_type} {self.variable} = {self.class_example_random_variable}.{self.method_1}({random_variable_2});
#     System.out.println({self.variable});'''
#         return self.get_class_main(class_main_body_with_return)
#
#     def get_code_with_int_and_without_methods(self):
#         return self.generate_class_example_with_int_type_and_without_methods() \
#             + self.generate_class_main_with_int_type_and_without_methods()
#
#     def generate_class_example_with_int_type_and_without_methods(self) -> str:
#         declared_variable = f'''{self.int_data_type} {self.variable};'''
#         return self.get_class_example(declared_variable)
#
#     def generate_class_main_with_int_type_and_without_methods(self) -> str:
#         class_example_random_variable_2 = self.get_random_variable()
#         class_main_with_int_type_and_without_methods = f'''
#     Example {self.class_example_random_variable} = new Example();
#     Example {class_example_random_variable_2} = {self.class_example_random_variable};
#     {self.class_example_random_variable}.{self.variable} = {self.random_value.get_int()};
#     {class_example_random_variable_2}.{self.variable} = {self.random_value.get_int()};
#     System.out.println({self.class_example_random_variable}.{self.variable} + " " + {class_example_random_variable_2}.{self.variable});
#         '''
#         return self.get_class_main(class_main_with_int_type_and_without_methods)
#
#
# if __name__ == '__main__':
#     g = GenerateJavaOOP()
#     # print(g.generate_code_with_int_type())
#     print(g.execute())
