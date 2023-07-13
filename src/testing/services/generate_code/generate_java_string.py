# from random import choice
#
# from testing.services.generate_code.config import Config
# from testing.utils.random_value import RandomValue
# from testing.utils.utils import remove_empty_paragraphs
#
#
# class GenerateJavaString:
#     config: Config = None
#     random_value: RandomValue = None
#     variable_1: str = None
#     variable_2: str = None
#     number: int = None
#     println: str = None
#     methods: list = None
#     random_string: str = ''
#     body: str = ''
#     code: str = None
#
#     def __init__(self):
#         self.config = Config()
#         self.random_value = RandomValue()
#         self.variable_1 = self.config.get_random_variable()
#         self.variable_2 = self.config.get_random_variable()
#         self.number = self.random_value.get_N_digits()
#         self.methods = [
#             self.generate_replace,
#             self.generate_compare_to,
#             self.generate_length,
#             self.generate_char_at,
#             self.generate_substring,
#             self.generate_index_of,
#             self.generate_last_index_of,
#             self.generate_concatenation,
#         ]
#
#     def execute(self):
#         choice(self.methods)()
#         self.generate_code()
#
#     def generate_replace(self) -> None:
#         self.generate_random_string()
#         find = self.random_value.get_digit()
#         replace = self.random_value.get_digit()
#         replacement = f'String {self.variable_2} = {self.variable_1}.replace("{find}", "{replace}");'
#         self.body = replacement
#         self.println = self.variable_2
#
#     def generate_code(self) -> None:
#         self.code = f'''
#     {self.random_string}
#     {self.body}
#     {self.get_print()}'''
#
#     def generate_random_string(self) -> None:
#         self.random_string = f'String {self.variable_1} = "{self.number}";'
#
#     def get_print(self) -> str:
#         return f'System.out.println({self.println});'
#
#     def generate_compare_to(self) -> None:
#         self.generate_random_string()
#         self.body = f'String {self.variable_2} = "{self.random_value.get_N_digits()}";'
#         self.println = f'{self.variable_1}.compareTo({self.variable_2})'
#
#     def generate_length(self) -> None:
#         self.generate_random_string()
#         length = f'int {self.variable_2} = {self.variable_1}.length();'
#         self.body = length
#         self.println = self.variable_2
#
#     def generate_char_at(self) -> None:
#         self.generate_random_string()
#         max_index = len(str(self.number)) - 1
#         random_digit = self.random_value.get_number_in_range(end=max_index)
#         self.println = f'{self.variable_1}.charAt({random_digit})'
#
#     def generate_substring(self) -> None:
#         self.generate_random_string()
#         argument = self.random_value.get_digit()
#         substring = f'String {self.variable_2} = {self.variable_1}.substring({argument});'
#         self.body = substring
#         self.println = self.variable_2
#
#     def generate_index_of(self) -> None:
#         self.generate_random_string()
#         argument = self.random_value.get_digit()
#         index_of = f'int {self.variable_2} = {self.variable_1}.indexOf("{argument}");'
#         self.body = index_of
#         self.println = self.variable_2
#
#     def generate_last_index_of(self) -> None:
#         self.generate_random_string()
#         argument = self.random_value.get_digit()
#         last_index_of = f'int {self.variable_2} = {self.variable_1}.lastIndexOf("{argument}");'
#         self.body = last_index_of
#         self.println = self.variable_2
#
#     def generate_concatenation(self) -> None:
#         digit_1 = self.random_value.get_digit()
#         digit_2 = self.random_value.get_digit()
#         concatenation = f'String {self.variable_1} = "x=" + {digit_1} + {digit_2};'
#         self.random_string = concatenation
#         self.println = self.variable_1
#
#     def get_code(self) -> str:
#         return remove_empty_paragraphs(self.code)
#
#
# if __name__ == '__main__':
#     GenerateJavaString = GenerateJavaString()
#     GenerateJavaString.execute()
