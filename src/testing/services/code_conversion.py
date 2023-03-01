import re


class JavaToPythonConversion:
    def __init__(self, code):
        self.code = code
        self.convert_code_to_python()
        # print(self.run_code())

    def convert_code_to_python(self):
        self.convert_do_while()
        self.convert_for()
        self.replace_symbols()
        self.convert_print()
        # print(self.code)

    def convert_do_while(self):
        start_symbol_do_while = 'do {'
        if self.is_symbol(start_symbol_do_while):
            do_while_boolean_expression = self.get_text_between_symbols('while (', ')')
            body_do_while = self.get_text_between_symbols(start_symbol_do_while, '}')
            self.code = self.code.replace('do', 'while True').replace(f'while ({do_while_boolean_expression})', '') \
                .replace(body_do_while, body_do_while + f'\tif {do_while_boolean_expression}: break')

    def convert_for(self):
        start_symbol_for = 'for ('
        if self.is_symbol(start_symbol_for):
            for_boolean_expression = self.get_text_between_symbols(start_symbol_for, ')')
            values_for = ', '.join([value_for for value_for in re.findall(r'\d+', for_boolean_expression)])
            python_for = f'for i in range({values_for})'
            self.code = self.code.replace(start_symbol_for + for_boolean_expression + ')', python_for)

    def convert_print(self):
        printed_variable = self.get_text_between_symbols('System.out.printIn("', ' =')
        variable_print_paragraph = self.code.split('\n')[-1]
        result = f'result = {printed_variable}'
        self.code = self.code.replace(variable_print_paragraph, result)

    def is_symbol(self, symbol):
        return self.code.find(symbol) != -1

    def get_text_between_symbols(self, start, end):
        return self.code.partition(start)[2].partition(end)[0]

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
