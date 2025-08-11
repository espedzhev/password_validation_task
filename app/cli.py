from enum import Enum
import sys

import click

from validation import is_valid_password


class PasswordCriteria(Enum):
    LENGTH = "Must be more than 8 characters long"
    UPPERCASE = "Must contain at least one uppercase letter"
    LOWERCASE = "Must contain at least one lowercase letter"
    DIGIT = "Must contain at least one digit"
    UNDERSCORE = "Must contain at least one underscore (_)"


def print_help() -> None:
    click.echo("Password Validation Criteria:")

    for criterion in PasswordCriteria:
        click.echo(f"- {criterion.value}")

    click.echo()


@click.command()
@click.option("--confirm", is_flag=True, help="Prompt for confirmation.")
def validate_password(confirm: bool) -> None:
    """
    CLI tool to validate a password.

    A valid password must meet the following criteria:
    - Be more than 8 characters long
    - Contain at least one uppercase letter
    - Contain at least one lowercase letter
    - Contain at least one digit
    - Contain at least one underscore (_)
    """
    print_help()

    password = click.prompt(
        "Enter your password",
        hide_input=True,
    )

    if confirm:
        confirm_password = click.prompt("Confirm your password", hide_input=True)

        if password != confirm_password:
            click.secho(
                "Passwords do not match.",
                fg="red",
            )
            sys.exit(1)

    click.echo("\nValidating your password...")

    if is_valid_password(password):
        click.secho(
            "Your password is valid!",
            fg="green",
        )
        sys.exit(0)
    else:
        click.secho(
            "Your password is invalid. Please ensure it meets all criteria.",
            fg="red",
        )
        sys.exit(1)


if __name__ == "__main__":
    validate_password()
