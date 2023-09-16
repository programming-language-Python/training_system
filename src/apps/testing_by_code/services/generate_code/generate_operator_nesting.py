from apps.testing_by_code import abstractions
from apps.testing_by_code.services.generate_code.check_for_looping import CheckForLooping
from apps.testing_by_code.utils.utils import add_tabs


class GenerateOperatorNesting(CheckForLooping, abstractions.Condition,
                              abstractions.Cycle):
    OLD = '}'

    def generate_cycle_nested_in_condition(self):
        condition = self.check_with_condition_priority()
        new = add_tabs(self.cycle) + '\n' + self.OLD
        return condition.replace(self.OLD, new)

    def generate_condition_nested_in_cycle(self):
        condition = self.check_with_cycle_priority()
        new = add_tabs(condition) + '\n' + self.OLD
        return self.cycle.replace(self.OLD, new)
