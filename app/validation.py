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


DEFAULT_RULES: tuple[tuple[str, Callable[[str], bool]], ...] = (
    ("min_length", min_length),
    ("require_uppercase", contains_uppercase),
    ("require_lowercase", contains_lowercase),
    ("require_digit", contains_digit),
    ("require_underscore", contains_underscore),
)


def evaluate_password_rules(
    password: str,
    rules: tuple[tuple[str, Callable[[str], bool]], ...] = DEFAULT_RULES,
) -> dict[str, bool]:
    """
    Returns a dict of rule_name: bool for each rule in rules
    """
    return {name: func(password) for name, func in rules}


def is_valid_password(
    password: str,
    rules: tuple[tuple[str, Callable[[str], bool]], ...] = DEFAULT_RULES,
) -> dict[str, bool] | bool:
    """
    Returns True if a password passes all rules, else False
    """
    rule_statuses = evaluate_password_rules(password, rules)

    return all(rule_statuses.values())
