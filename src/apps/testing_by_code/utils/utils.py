import re
from typing import Mapping


def add_tabs(text: str) -> str:
    return '\n'.join(f'\t{word}' for word in text.split('\n'))


def remove_empty_paragraphs(text):
    return re.sub('\s+\n+', '\n', text)


def get_list_dictionary_keys(dictionary: Mapping) -> list:
    return list(dictionary.keys())
