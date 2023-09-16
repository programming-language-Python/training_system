from typing import Mapping

DEFAULT_TYPE = 'int'
INTEGER_DATA_TYPES = ['byte', 'short', 'int', 'long']
REAL_DATA_TYPES = ['float', 'double']
NUMERIC_DATA_TYPES = INTEGER_DATA_TYPES + REAL_DATA_TYPES
COMPARISON_OPERATORS = ['<', '<=', '>', '>=', '==', '!=']
LOGICAL_OPERATORS = ['&&', '||']
INCREMENT_ARITHMETIC_OPERATORS = ['+', '*']
DECREMENT_ARITHMETIC_OPERATORS = ['-', '/']
ARITHMETIC_OPERATORS = INCREMENT_ARITHMETIC_OPERATORS + \
                       DECREMENT_ARITHMETIC_OPERATORS
arithmetic_operator = ''
COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS = {
    '<': INCREMENT_ARITHMETIC_OPERATORS,
    '<=': INCREMENT_ARITHMETIC_OPERATORS,
    '>': DECREMENT_ARITHMETIC_OPERATORS,
    '>=': DECREMENT_ARITHMETIC_OPERATORS,
    '==': '',
    '!=': ''
}


def get_greater_and_less_comparison_operators() -> Mapping[str, str]:
    greater_and_less_comparison_operators = \
        COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS.copy()
    del greater_and_less_comparison_operators['==']
    del greater_and_less_comparison_operators['!=']
    return greater_and_less_comparison_operators
