from dataclasses import dataclass
from enum import Enum

from django.db.models import QuerySet

Weight = int


class ConditionType(str, Enum):
    SIMPLE = 'Простое'
    COMPOSITE = 'Составное'


class NestingType(QuerySet):
    IF_IN_CYCLE = 'Оператор if вложен в цикл'
    CYCLE_IN_IF = 'Цикл вложен в оператор if'


class Cycle(QuerySet):
    WHILE = 'while'
    DO_WHILE = 'do-while'
    FOR = 'for'


@dataclass
class Setting:
    is_if_operator: bool
    condition_of_if_operator: ConditionType
    cycle: Cycle
    cycle_condition: ConditionType
    operator_nesting: NestingType
    is_OOP: bool
    is_strings: bool


class DataType(str, Enum):
    INT = 'int'
    DOUBLE = 'double'
    LONG = 'long'
    FLOAT = 'float'


Name = str


@dataclass
class Variable:
    name: Name
    data_type: DataType
    value: int
    value_in_condition: int | None = None
    arithmetic_operation_in_condition: str | None = None
    value_in_cycle: int | None = None
    arithmetic_operation_in_cycle: str | None = None

    def get_expression_in_cycle(self) -> str:
        return f'{self.name} {self.arithmetic_operation_in_cycle}= ' \
               f'{self.value_in_cycle}'

    def get_expression_in_if(self) -> str:
        return f'{self.name} {self.arithmetic_operation_in_condition}= ' \
               f'{self.value_in_condition}'
