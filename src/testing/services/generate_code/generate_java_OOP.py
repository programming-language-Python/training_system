from random import choice
from testing.services.generate_code.config import Config, get_readable_variables
from testing.utils.random_value import RandomValue


class GenerateJavaOOP:
    def __init__(self) -> None:
        self.variables = get_readable_variables()
        self.random_value = RandomValue()
        self.random_numeric_data_type = choice(Config.NUMERIC_DATA_TYPES)
        self.random_int_data_type = choice(Config.INTEGER_DATA_TYPES)
        self.random_real_data_type = choice(Config.REAL_DATA_TYPES)
        self.random_variable = self.get_random_variable()
        self.random_method_1 = self.get_random_variable()
        self.random_method_2 = self.get_random_variable()
        self.class_example_random_variable = self.get_random_variable()
        self.random_method_type = choice(Config.INTEGER_DATA_TYPES)
        self.random_variable_type_1 = choice(Config.INTEGER_DATA_TYPES)
        self.random_variable_type_2 = choice(Config.INTEGER_DATA_TYPES)

    def get_random_variable(self) -> str:
        random_variable = choice(self.variables)
        self.variables = self.variables.replace(random_variable, '')
        return random_variable

    def execute(self) -> str:
        is_integer_data_type = any(map(lambda v: v in self.random_numeric_data_type, Config.INTEGER_DATA_TYPES))
        if is_integer_data_type:
            return self.get_code_with_int_type()
        return self.generate_code_with_float_type()

    def get_code_with_int_type(self) -> str:
        return self.generate_class_example_with_int_type() + self.generate_class_main_with_int_type()

    def generate_class_example_with_int_type(self) -> str:
        declared_variable = f'''{self.random_numeric_data_type} {self.random_variable};'''
        class_example_body_with_int_type = declared_variable + f'''
    Example({self.random_numeric_data_type} {self.random_variable}){'{'}
        this.{self.random_variable} = {self.random_variable};
    {'}'}
    void {self.random_method_1}({self.random_numeric_data_type} {self.random_variable}){'{'}
        {self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_int()};
    {'}'}
    void {self.random_method_2}(Example {self.class_example_random_variable}){'{'}
        {self.class_example_random_variable}.{self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_int()};
    {'}'}'''
        return self.get_class_example(class_example_body_with_int_type)

    def generate_class_main_with_int_type(self) -> str:
        random_argument = choice([self.random_variable, self.class_example_random_variable])
        random_method = self.random_method_1 if random_argument == self.random_variable else self.random_method_2
        class_example_name = ''
        if random_argument == self.class_example_random_variable:
            class_example_name = f'''{self.class_example_random_variable}.'''

        class_main_body_with_int_type = f'''
    {self.random_numeric_data_type} {self.random_variable} = {self.random_value.get_random_int()};
    Example {self.class_example_random_variable} = new Example({self.random_variable});
    {self.class_example_random_variable}.{random_method}({random_argument});
    System.out.println({class_example_name}{self.random_variable});'''
        return class_main_body_with_int_type

    @staticmethod
    def get_class_example(body: str) -> str:
        return f'''
class Example {'{'}
    {body}
{'}'}'''

    @staticmethod
    def get_class_main(body: str) -> str:
        return f'''
public class Main {'{'}
    public static void main(String[] args) {'{'}
        {body}
    {'}'}
{'}'}'''

    def generate_code_with_float_type(self) -> str:
        is_float_data_type = 'float' in self.random_numeric_data_type
        if is_float_data_type:
            suffix = 'f'
        else:
            suffix = ''
        class_example_body = f'''
        {self.random_numeric_data_type} {self.random_variable};
        Example({self.random_numeric_data_type} {self.random_variable}){'{'}
            this.{self.random_variable} = {self.random_variable};
        {'}'}
        void {self.random_method_1}({self.random_numeric_data_type} {self.random_variable}){'{'}
            {self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_number()}{suffix};
        {'}'}
        void {self.random_method_2}(Example {self.class_example_random_variable}){'{'}
            {self.class_example_random_variable}.{self.random_variable} {choice(Config.ARITHMETIC_OPERATORS)}= {self.random_value.get_random_number()}{suffix};
        {'}'}'''
        class_main_body = f'''
        {self.random_numeric_data_type} {self.random_variable} = {self.random_value.get_random_number()}{suffix};
        Example {self.class_example_random_variable} = new Example({self.random_variable});
        {self.class_example_random_variable}.{self.random_method_1}({self.random_variable});
        System.out.println({self.random_variable});'''
        return self.get_class_example(class_example_body) + self.get_class_main(class_main_body)

    def get_code_2(self):
        return self.generate_class_example_with_return() + self.generate_class_main_with_return()

    def generate_class_example_with_return(self) -> str:
        class_example_body_with_return = f'''
        {self.random_method_type} {self.random_method_1}(){'{'}
            return {self.random_value.get_random_int()};
        {'}'}
        {self.random_method_type} {self.random_method_1}({self.random_variable_type_1} {self.random_variable}){'{'}
            return {self.random_value.get_random_int()};
        {'}'}
        {self.random_method_type} {self.random_method_1}({self.random_variable_type_2} {self.random_variable}){'{'}
            return {self.random_value.get_random_int()};
        {'}'}'''
        return self.get_class_example(class_example_body_with_return)

    def generate_class_main_with_return(self) -> str:
        random_variable_type = choice([self.random_variable_type_1, self.random_variable_type_2])
        variables = [self.get_random_variable(), '']
        random_variable_2 = choice(variables)
        initialized_variable = ''
        is_variable_2 = random_variable_2 != ''
        if is_variable_2:
            initialized_variable = f'''{random_variable_type} {random_variable_2} = {RandomValue.get_random_int()};'''
        class_main_body_with_return = f'''
    Example {self.class_example_random_variable} = new Example();
    {initialized_variable}
    {self.random_method_type} {self.random_variable} = {self.class_example_random_variable}.{self.random_method_1}({random_variable_2});
    System.out.println({self.random_variable});'''
        return self.get_class_main(class_main_body_with_return)

    def get_code_3(self):
        return self.generate_class_example_with_int_type_and_without_methods() \
            + self.generate_class_main_with_int_type_and_without_methods()

    def generate_class_example_with_int_type_and_without_methods(self) -> str:
        declared_variable = f'''{self.random_int_data_type} {self.random_variable};'''
        return self.get_class_example(declared_variable)

    def generate_class_main_with_int_type_and_without_methods(self) -> str:
        class_example_random_variable_2 = self.get_random_variable()
        class_main_with_int_type_and_without_methods = f'''
    Example {self.class_example_random_variable} = new Example();
    Example {class_example_random_variable_2} = {self.class_example_random_variable};
    {self.class_example_random_variable}.{self.random_variable} = {self.random_value.get_random_int()};
    {class_example_random_variable_2}.{self.random_variable} = {self.random_value.get_random_int()};
    System.out.println({self.class_example_random_variable}.{self.random_variable} + " " + {class_example_random_variable_2}.{self.random_variable});
        '''
        return self.get_class_main(class_main_with_int_type_and_without_methods)


if __name__ == '__main__':
    g = GenerateJavaOOP()
    # print(g.generate_code_with_int_type())
    print(g.get_code_3())
