from enum import Enum

import pytest
from app.validation import is_valid_password


class PasswordExamples(Enum):
    VALID = "Strong_Pass1"
    TOO_SHORT = "short1_"
    NO_NUMBER = "NoNumber_"
    NO_UPPERCASE = "nonumber_"
    NO_LOWERCASE = "NONUMBER1_"
    NO_UNDERSCORE = "NoUnderscore1"
    EMPTY = ""


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
    ],
)
def test_is_valid_password(password_enum: PasswordExamples, expected: bool):
    assert is_valid_password(password_enum.value) == expected
