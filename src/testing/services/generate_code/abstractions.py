import string
from collections import OrderedDict
from random import randint, choice

from testing.services.generate_code import types, config
from testing.services.generate_code.config import COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS
from testing.utils.random_value import get_positive_int


class Variable:
    info: dict[types.Name, types.Variable] = OrderedDict()
    count: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.variables = self._get_readable_variables()

    @staticmethod
    def _get_readable_variables() -> str:
        variables = string.ascii_letters
        excluded_variables = ['i', 'l', 'o', 'O']
        for variable in excluded_variables:
            variables = variables.replace(variable, '')
        return variables

    # def get(self, name: Name) -> Variable:
    #     return self.info[name]

    def generate_variables(self) -> str:
        count = randint(2, 3)
        variables = ''
        for i in range(count):
            self.add()
            variables += self._generate_variable()
        return variables

    def add(self) -> None:
        name = self._get_variable()
        data_type = config.DEFAULT_TYPE
        value = get_positive_int()
        variable = types.Variable(name, data_type, value)
        self.set(variable)

    def _get_variable(self) -> str:
        try:
            variable = choice(self.variables)
        except IndexError:
            self.variables = self._get_readable_variables()
            variable = choice(self.variables)
        self.variables = self.variables.replace(variable, '')
        return variable

    def set(self, variable: types.Variable) -> None:
        name = variable.name
        self.info[name] = variable

    def _generate_variable(self) -> str:
        info_about_last_variable = list(self.info.items())[-1][1]
        data_type = info_about_last_variable.data_type
        name = info_about_last_variable.name
        value = info_about_last_variable.value
        return f'{data_type} {name} = {value};\n'

    def get_random_used_variable(self) -> str:
        return choice(list(self.info.keys()))

    def set_value_in_condition(self, name: types.Name, value: int) -> None:
        self.info[name].value_in_condition = value

    def set_arithmetic_operation_in_condition(self, name: types.Name,
                                              arithmetic_operation: str):
        self.info[name].arithmetic_operation_in_condition = \
            arithmetic_operation

    def set_value_in_cycle(self, name: types.Name, value: int) -> None:
        self.info[name].value_in_cycle = value

    def set_arithmetic_operation_in_cycle(self, name: types.Name,
                                          arithmetic_operation: str):
        self.info[name].arithmetic_operation_in_cycle = arithmetic_operation

    def set_arithmetic_operation_in_cycle_having_comparison_operator(self, name: types.Name,
                                                                     comparison_operator: str):
        arithmetic_operations = COMPARISON_BOUND_TO_ARITHMETIC_OPERATORS[comparison_operator]
        arithmetic_operation = choice(arithmetic_operations)
        self.info[name].arithmetic_operation_in_cycle = arithmetic_operation

    def get_info(self):
        return self.info

    def get_count(self) -> int:
        return len(self.info)

    def clear(self) -> None:
        self.variables = self._get_readable_variables()
        self.info.clear()


class Setting:
    def __init__(self, setting: types.Setting, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setting = setting

    def get_setting(self) -> types.Setting:
        return self.setting


class Condition:
    def __init__(self, condition: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.condition = condition


class Cycle:
    def __init__(self, cycle: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cycle = cycle
