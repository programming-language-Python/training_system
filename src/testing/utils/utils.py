import re
from typing import Mapping


def round_up(num: [int, float]) -> int:
    return int(num + (0.5 if num > 0 else -0.5))


def write_to_file(name: str, text: str) -> None:
    with open(name, 'w') as file:
        file.write(text)


def add_tabs(text: str) -> str:
    return '\n'.join(f'\t{word}' for word in text.split('\n'))


def remove_empty_paragraphs(text):
    return re.sub('\s+\n+', '\n', text)


def get_list_dictionary_keys(dictionary: Mapping) -> list:
    return list(dictionary.keys())
