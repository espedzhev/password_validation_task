from enum import Enum
from typing import cast

import click
import pytest
from click.testing import CliRunner
from app.cli import PasswordCriteria, validate_password
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


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_validate_password_valid_input(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.VALID.value}\n{PasswordExamples.VALID.value}\n",
    )

    assert result.exit_code == 0
    assert "✅ Your password is valid!" in result.output


def test_cli_validate_password_invalid_input(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.TOO_SHORT.value}\n{PasswordExamples.TOO_SHORT.value}\n",
    )

    assert result.exit_code == 0
    assert "❌ Your password is invalid" in result.output


def test_cli_help_text_displayed(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.VALID.value}\n{PasswordExamples.VALID.value}\n",
    )

    for criterion in PasswordCriteria:
        assert criterion.value in result.output


def test_cli_mismatched_passwords(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.VALID.value}\n{PasswordExamples.NO_NUMBER.value}\n",
    )

    assert result.exit_code == 0
    assert "❌ Your password is invalid" in result.output
