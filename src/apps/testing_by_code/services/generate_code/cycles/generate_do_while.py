from apps.testing_by_code.services.generate_code.cycles.generate_while import GenerateWhile
from apps.testing_by_code.types import ConditionType


class GenerateDoWhile(GenerateWhile):
    def execute(self, condition_type: ConditionType) -> str:
        condition = self._get_condition(condition_type)
        body = self._generate_body_with_variables_bound_to_arithmetic_operators()
        template = f'''
do {'{'} 
    {body}
{'}'}
while ({condition});'''
        return template
