from testing.utils.utils import add_tabs


def get_template_class_example(body: str) -> str:
    return f'''
class Example {'{'}
    {body}
{'}'}'''


def get_template_class_main(body: str) -> str:
    return f'''
public class Main {'{'}
    public static void main(String[] args) {'{'}
        {add_tabs(body)}
    {'}'}
{'}'}'''


def get_string_template(string, body, print_) -> str:
    return f'{string}\n{body}\n{get_print_template(text=print_)}'


def get_string_template_without_body(string, print_) -> str:
    return f'{string}\n{get_print_template(text=print_)}'


def get_print_template(text: str):
    return f'\nSystem.out.println({text});'
