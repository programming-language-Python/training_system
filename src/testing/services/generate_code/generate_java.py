from random import choice

from testing.utils.utils import remove_empty_paragraphs
from .OOP.OOP import generate_java_OOP
from .check_for_looping import CheckForLooping
from .cycles.generate_do_while import GenerateDoWhile
from .cycles.generate_for import GenerateFor
from .generate_if import GenerateIf
from .cycles.generate_while import GenerateWhile
from .generate_java_work_with_strings import GenerateJavaWorkWithStrings
from .generate_operator_nesting import GenerateOperatorNesting
from .templates import get_print_template
from ... import abstractions
from ...types import NestingType, OperatorPresenceType


class GenerateJava(abstractions.Setting, abstractions.Variable):
    body: str = ''

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute(self) -> str:
        code = ''
        if self.setting.is_OOP:
            return generate_java_OOP()
        if self.setting.is_strings:
            return self.get_java_string()
        code += self.generate_variables()
        if self.setting.operator_nesting:
            code += self.get_nesting_of_operators()
        else:
            code += self.get_operator()
        code += self.generate_print_of_variable()
        self.clear()
        return remove_empty_paragraphs(code)

    @staticmethod
    def get_java_string() -> str:
        generate_java_string = GenerateJavaWorkWithStrings()
        return generate_java_string.execute()

    def get_nesting_of_operators(self) -> str:
        operator_nesting = choice(self.setting.operator_nesting).title
        is_if_in_cycle = operator_nesting == NestingType.IF_IN_CYCLE
        if is_if_in_cycle:
            return self._get_condition_nested_in_cycle()
        else:
            return self._get_cycle_nested_in_condition()

    def _get_condition_nested_in_cycle(self) -> str:
        generate_operator_nesting = GenerateOperatorNesting(
            condition=self.get_condition(),
            cycle=self.get_cycle()
        )
        return generate_operator_nesting.generate_condition_nested_in_cycle()

    def _get_cycle_nested_in_condition(self) -> str:
        # TODO variable_service избыточна?
        generate_operator_nesting = GenerateOperatorNesting(
            condition=self.get_condition(),
            cycle=self.get_cycle()
        )
        return generate_operator_nesting.generate_cycle_nested_in_condition()

    def get_operator(self) -> str:
        is_condition = self.setting.is_if_operator == OperatorPresenceType \
            .BE_PRESENT
        is_cycle = self.setting.cycle
        if is_condition and is_cycle:
            return self._get_random_order_of_operators()
        if is_condition:
            return self.get_condition()
        if is_cycle:
            return self.get_cycle()

    # TODO сделать на проверку бесконечного выполнения
    def _get_random_order_of_operators(self) -> str:
        operators = [self.get_condition(), self.get_cycle()]
        operator_1 = choice(operators)
        operators.remove(operator_1)
        operator_2 = operators[0]

        if 'if' in operator_1:
            check_for_looping = CheckForLooping(condition=operator_1)
            operator_1 = check_for_looping.check_with_condition_priority()

        random_order_of_operators = operator_1 + operator_2
        return random_order_of_operators

    def get_condition(self) -> str:
        generate_if = GenerateIf()
        condition = generate_if.execute(
            self.setting.condition_of_if_operator
        )
        return condition

    def get_cycle(self) -> str:
        operator = choice(self.setting.cycle).title
        if operator == 'while':
            return self._get_while()
        if operator == 'do-while':
            return self._get_do_while()
        if operator == 'for':
            return self._get_for()

    # TODO Разобраться с condition_type и self.setting
    def _get_while(self) -> str:
        generate_while = GenerateWhile()
        condition_type = self.setting.cycle_condition
        while_ = generate_while.execute(condition_type)
        return while_

    def _get_do_while(self) -> str:
        generate_do_while = GenerateDoWhile()
        condition_type = self.setting.cycle_condition
        do_while = generate_do_while.execute(condition_type)
        return do_while

    def _get_for(self) -> str:
        generate_for = GenerateFor()
        condition_type = self.setting.cycle_condition
        for_ = generate_for.execute(condition_type)
        return for_

    def generate_print_of_variable(self) -> str:
        list_variables = list(self.get_info())
        variable = choice(list_variables)
        return get_print_template(text=variable)
