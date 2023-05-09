from random import choice
from testing.services.generate_code.config import Config
from generate_java import GenerateJava
from testing.utils.random_value import RandomValue


class GenerateJavaOOP:
    def __init__(self) -> None:
        self.random_value = RandomValue()
        self.random_numeric_data_type = choice(Config.NUMERIC_DATA_TYPES)
        self.random_variable = choice(GenerateJava.get_readable_variables())
        self.random_method_1 = choice(GenerateJava.get_readable_variables())
        self.random_method_2 = choice(GenerateJava.get_readable_variables())
        self.second_class_random_variable = choice(GenerateJava.get_readable_variables())

    def execute(self) -> str:
        is_integer_data_type = any(map(lambda v: v in self.random_numeric_data_type, Config.INTEGER_DATA_TYPES))
        if is_integer_data_type:
            return self.get_code_with_int_type()
        return self.get_code_with_float_type()

    def get_code_with_int_type(self) -> str:
        return f'''
            class Example {'{'}
                {self.random_numeric_data_type} {self.random_variable};
                Example({self.random_numeric_data_type} {self.random_variable}){'{'}
                    this.{self.random_variable} = {self.random_variable};
                {'}'}
                void {self.random_method_1}({self.random_numeric_data_type} {self.random_variable}){'{'}
                    {self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_int()};
                {'}'}
                void {self.random_method_2}(Example {self.second_class_random_variable}){'{'}
                    {self.second_class_random_variable}.{self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_int()};
                {'}'}
            {'}'}
            public class Main {'{'}
                public static void main(String[] args) {'{'}
                    {self.random_numeric_data_type} {self.random_variable} = {self.random_value.get_random_int()};
                    Example {self.second_class_random_variable} = new Example({self.random_variable});
                    {self.second_class_random_variable}.{self.random_method_1}({self.random_variable});
                    System.out.println({self.random_variable});
                {'}'}
            {'}'}'''

    def get_code_with_float_type(self) -> str:
        is_float_data_type = 'float' in self.random_numeric_data_type
        if is_float_data_type:
            suffix = 'f'
        else:
            suffix = ''
        return f'''
            class Example {'{'}
                {self.random_numeric_data_type} {self.random_variable};
                Example({self.random_numeric_data_type} {self.random_variable}){'{'}
                    this.{self.random_variable} = {self.random_variable};
                {'}'}
                void {self.random_method_1}({self.random_numeric_data_type} {self.random_variable}){'{'}
                    {self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_number()}{suffix};
                {'}'}
                void {self.random_method_2}(Example {self.second_class_random_variable}){'{'}
                    {self.second_class_random_variable}.{self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_number()}{suffix};
                {'}'}
            {'}'}
            public class Main {'{'}
                public static void main(String[] args) {'{'}
                    {self.random_numeric_data_type} {self.random_variable} = {self.random_value.get_random_number()}{suffix};
                    Example {self.second_class_random_variable} = new Example({self.random_variable});
                    {self.second_class_random_variable}.{self.random_method_1}({self.random_variable});
                    System.out.println({self.random_variable});
                {'}'}
            {'}'}'''


if __name__ == '__main__':
    g = GenerateJavaOOP()
    print(g.execute())
