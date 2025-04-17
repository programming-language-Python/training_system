def round_up(num: [int, float]) -> int:
    return int(num + (0.5 if num > 0 else -0.5))
