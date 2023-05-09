def round_up(num) -> int:
    return int(num + (0.5 if num > 0 else -0.5))


def write_to_file(name, text):
    with open(name, 'w') as file:
        file.write(text)
