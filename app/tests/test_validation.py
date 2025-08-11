from enum import Enum

import pytest
from app.validation import is_valid_password, evaluate_password_rules


class PasswordExamples(Enum):
    VALID = "Strong_Pass1"
    TOO_SHORT = "short1_"
    NO_NUMBER = "NoNumber_"
    NO_UPPERCASE = "nonumber_"
    NO_LOWERCASE = "NONUMBER1_"
    NO_UNDERSCORE = "NoUnderscore1"
    EMPTY = ""
    EXACT_EIGHT = "Abcdef1_"  # 8 chars
    NINE_CHARS = "Abcdefg1_"  # 9 chars


@pytest.mark.parametrize(
    "password_enum, expected",
    [
        (PasswordExamples.VALID, True),
        (PasswordExamples.TOO_SHORT, False),
        (PasswordExamples.NO_NUMBER, False),
        (PasswordExamples.NO_UPPERCASE, False),
        (PasswordExamples.NO_LOWERCASE, False),
        (PasswordExamples.NO_UNDERSCORE, False),
        (PasswordExamples.EMPTY, False),
        (PasswordExamples.EXACT_EIGHT, False),
        (PasswordExamples.NINE_CHARS, True),
    ],
)
def test_is_valid_password(password_enum: PasswordExamples, expected: bool):
    assert is_valid_password(password_enum.value) == expected


def test_detailed_rules():
    pwd = "lowercase1"  # missing uppercase and underscore
    rules = evaluate_password_rules(pwd)
    assert isinstance(rules, dict)
    assert rules["min_length"] is True
    assert rules["require_lowercase"] is True
    assert rules["require_digit"] is True
    assert rules["require_uppercase"] is False
    assert rules["require_underscore"] is False
