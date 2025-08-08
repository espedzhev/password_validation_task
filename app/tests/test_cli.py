from typing import cast

import click
import pytest
from click.testing import CliRunner

from app.cli import validate_password, PasswordCriteria
from .test_validation import PasswordExamples


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_validate_password_valid_input(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.VALID.value}\n",
    )

    assert result.exit_code == 0
    assert "Your password is valid!" in result.output


def test_cli_validate_password_invalid_input(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.TOO_SHORT.value}\n",
    )

    assert result.exit_code == 0
    assert "Your password is invalid" in result.output


def test_cli_help_text_displayed(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        input=f"{PasswordExamples.VALID.value}\n",
    )

    for criterion in PasswordCriteria:
        assert criterion.value in result.output


def test_cli_mismatched_passwords(runner):
    result = runner.invoke(
        cast(click.Command, validate_password),
        args="--confirm",
        input=f"{PasswordExamples.VALID.value}\n{PasswordExamples.NO_NUMBER.value}\n",
    )

    assert result.exit_code == 0
    assert "Passwords do not match" in result.output
