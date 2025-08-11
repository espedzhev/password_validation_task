from typing import Callable


def min_length(password: str, length: int = 8) -> bool:
    return len(password) > length


def contains_uppercase(password: str) -> bool:
    return any(char.isupper() for char in password)


def contains_lowercase(password: str) -> bool:
    return any(char.islower() for char in password)


def contains_digit(password: str) -> bool:
    return any(char.isdigit() for char in password)


def contains_underscore(password: str) -> bool:
    return "_" in password


def is_valid_password(
    password: str,
    rules: dict[str, Callable[[str], bool]] | None = None,
    detailed: bool = False,
) -> dict[str, bool] | bool:
    rules = rules or {
        "min_length": min_length,
        "require_uppercase": contains_uppercase,
        "require_lowercase": contains_lowercase,
        "require_digit": contains_digit,
        "require_underscore": contains_underscore,
    }

    rule_statuses = {name: func(password) for name, func in rules.items()}

    if detailed:
        return rule_statuses

    return all(rule_statuses.values())
