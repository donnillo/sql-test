import re

camel_to_snake_regex = re.compile(
    r"""
        (?:[A-Z0-9]+(?![a-z])) |  # All caps without following non-caps |
        (?:[A-Z]{1}[a-z]+) |      # Single capital followed by non-caps |
        (?:[A-Za-z0-9]+)          # Any alphanumeric                    V
    """,
    re.VERBOSE
)


def camel_to_words(name: str) -> list[str]:
    return camel_to_snake_regex.findall(name)


def camel_to_snake(name: str) -> str:
    return '_'.join(map(str.lower, camel_to_words(name)))
