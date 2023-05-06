import re

from testing.services.code_generation import RandomizerJava


class JavaToPythonConversion:
    def __init__(self, code):
        print(code)
        self.code = code
        self.variables = self.get_variables()
        self.convert_code_to_python()
        print(self.code)

    def get_variables(self):
        return self.get_text_between_symbols('#variables_used:', '\n').split()

    def convert_code_to_python(self):
        self.remove_carriage_return()
        self.convert_do_while()
        self.convert_for()
        self.convert_arithmetic_operators()
        self.replace_symbols()
        self.convert_print()

    def remove_carriage_return(self):
        self.code = self.code.replace('\r', '')

    def convert_do_while(self):
        start_symbol_do_while = 'do {'
        if self.is_symbol(start_symbol_do_while):
            do_while_boolean_expression = self.get_text_between_symbols('while (', ')')
            characters_between_while_and_closing_bracket = self.get_text_between_symbols(
                '}',
                f'while ({do_while_boolean_expression})'
            )
            self.code = self.code.replace('do', 'while True') \
                .replace(f'while ({do_while_boolean_expression})',
                         f'\tif {do_while_boolean_expression}: continue'
                         f'{characters_between_while_and_closing_bracket}\telse: break')

    def convert_for(self):
        start = 'for ('
        if self.is_symbol(start):
            end = ') {'
            for_boolean_expression = self.get_text_between_symbols(start, end)
            values_for = [value_for for value_for in re.findall(r'\d+', for_boolean_expression)]
            values_for.pop(2)
            operator_less_or_equal = for_boolean_expression.find('i <=') != -1
            operator_greater_or_equal = for_boolean_expression.find('i >=') != -1
            is_increase_max_value = operator_less_or_equal or operator_greater_or_equal
            if is_increase_max_value:
                values_for[1] = str(int(values_for[1]) + 1)
            for_python = f'for i in range({", ".join(values_for)})'
            self.convert_compound_for(for_boolean_expression)
            self.code = self.code.replace(start + for_boolean_expression + ')', for_python)

    def convert_compound_for(self, for_boolean_expression):
        is_compound_for = for_boolean_expression.find('&&') != -1 or for_boolean_expression.find('||') != -1
        if is_compound_for:
            start_and_end = '; '
            condition_in_for = self.get_text_between_symbols(start_and_end, start_and_end)
            body_for = self.get_text_between_symbols(for_boolean_expression + ') {\n', '}')
            indent_size_in_body = body_for.split('\n')[0].count('\t')
            body_for_with_tabs_added = RandomizerJava.add_tabs_to_paragraphs(body_for)
            body_for_python = '\t' * indent_size_in_body + f'if {condition_in_for}:\n{body_for_with_tabs_added}'
            self.code = self.code.replace(body_for, body_for_python)

    def convert_print(self):
        printed_variable = self.get_text_between_symbols('System.out.println("', ' =')
        variable_print_paragraph = self.code.split('\n')[-1]
        result = f'result = int({printed_variable})'
        self.code = self.code.replace(variable_print_paragraph, result)

    def is_symbol(self, symbol):
        return self.code.find(symbol) != -1

    def get_text_between_symbols(self, start, end):
        return self.code.partition(start)[2].partition(end)[0]

    def convert_arithmetic_operators(self):
        for variable in self.variables:
            self.get_text_between_symbols()

    def replace_symbols(self):
        deleting_symbol = ''
        replacement_symbols = {
            ' {': ':',
            '\t}': deleting_symbol,
            '}\n': deleting_symbol,
            '}': deleting_symbol,
            'int ': deleting_symbol,
            ';': deleting_symbol,
            '&&': 'and',
            '||': 'or'
        }
        for symbol, replacement in replacement_symbols.items():
            self.code = self.code.replace(symbol, replacement)

    def run_code(self):
        context = {}
        exec(self.code, context)
        return round(context['result'], 2)


if __name__ == "__main__":
    code = 'int D = 70;\nint h = 69;\nfor (int i = 9; i >= 9 && D != 40; i/=9){\n\tD *= 85;\n\tif (D == 12 || h == 9){\n\t\tD /= 41;\n\t}\n}\nSystem.out.println("h = " + h);'
    # code = 'int d = 70;\nint e = 80\nSystem.out.println("d = " + d);'
    JavaToPythonConversion(code)
