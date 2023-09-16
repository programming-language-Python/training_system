from typing import Protocol

from apps.testing_by_code.types import Variable


class IBody(Protocol):
    def generate_body(self) -> str:
        raise NotImplementedError


class ICondition(Protocol):
    def get_condition(self) -> str:
        raise NotImplementedError


class ISimpleCondition(Protocol):
    def generate_simple_condition(self) -> str:
        raise NotImplementedError


class ICompoundCondition(Protocol):
    def generate_compound_condition(self) -> str:
        raise NotImplementedError


class IOperatorNesting(Protocol):
    def get_current_or_new_condition(self) -> str:
        raise NotImplementedError

    def get_new_condition(self, variable_data: Variable,
                          arithmetic_operator: str) -> str:
        raise NotImplementedError


class IOop(Protocol):
    def get_class_example(self) -> str:
        raise NotImplementedError

    def generate_class_example_body(self) -> str:
        raise NotImplementedError

    def get_class_main(self) -> str:
        raise NotImplementedError

    def generate_class_main_body(self) -> str:
        raise NotImplementedError
