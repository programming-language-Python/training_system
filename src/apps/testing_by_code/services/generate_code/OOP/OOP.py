from random import choice

from apps.testing_by_code.services.generate_code.OOP.generate_OOP_with_methods import \
    GenerateOOPWithMethods
from apps.testing_by_code.services.generate_code.OOP.generate_OOP_with_return import \
    GenerateOOPWithReturn
from apps.testing_by_code.services.generate_code.OOP.generate_OOP_without_methods import \
    GenerateOOPWithoutMethods
from apps.testing_by_code.utils.utils import remove_empty_paragraphs


def generate_java_OOP() -> str:
    codes = [
        _get_OOP_with_methods,
        _get_OOP_without_methods,
        _get_OOP_with_return
    ]
    code = choice(codes)
    return remove_empty_paragraphs(code())


def _get_OOP_with_methods() -> str:
    generate_OOP_with_methods = GenerateOOPWithMethods()
    return generate_OOP_with_methods.execute()


def _get_OOP_without_methods() -> str:
    generate_OOP_without_methods = GenerateOOPWithoutMethods()
    return generate_OOP_without_methods.execute()


def _get_OOP_with_return() -> str:
    generate_OOP_with_return = GenerateOOPWithReturn()
    return generate_OOP_with_return.execute()


if __name__ == '__main__':
    # print(generate_java_OOP())
    print(_get_OOP_with_methods())
