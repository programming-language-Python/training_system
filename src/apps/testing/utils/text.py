import re


def convert_from_PascalCase_to_snake_case(text: str) -> str:
    return re.sub('(?<!^)(?=[A-Z])', '_', text).lower()
