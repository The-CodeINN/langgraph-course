def add(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: The first number.
        b: The second number.
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers.

    Args:
        a: The first number.
        b: The second number.
    """
    return a - b


def square(a: int) -> int:
    """
    Square a number.

    Args:
        a: The number to square.
    """
    return a**2


tools = [add, subtract, square]
