class Config:
    INTEGER_DATA_TYPES = ['byte', 'short', 'int', 'long']
    REAL_DATA_TYPES = ['float', 'double']
    NUMERIC_DATA_TYPES = INTEGER_DATA_TYPES + REAL_DATA_TYPES
    COMPARISON_OPERATORS = ['<', '<=', '>', '>=', '==', '!=']
    LOGICAL_OPERATORS = ['&&', '||']
    INCREMENT_ARITHMETIC_OPERATORS = ['+', '*']
    DECREMENT_ARITHMETIC_OPERATORS = ['-', '/']
    ARITHMETIC_OPERATORS = INCREMENT_ARITHMETIC_OPERATORS + DECREMENT_ARITHMETIC_OPERATORS
    arithmetic_operators_used = []
    arithmetic_operator = ''
    COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS = {
        '<': INCREMENT_ARITHMETIC_OPERATORS,
        '<=': INCREMENT_ARITHMETIC_OPERATORS,
        '>': DECREMENT_ARITHMETIC_OPERATORS,
        '>=': DECREMENT_ARITHMETIC_OPERATORS,
        '==': '',
        '!=': ''
    }
