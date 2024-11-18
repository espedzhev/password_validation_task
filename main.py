from enum import Enum

import click


class PasswordCriteria(Enum):
    LENGTH = "Must be more than 8 characters long"
    UPPERCASE = "Must contain at least one uppercase letter"
    LOWERCASE = "Must contain at least one lowercase letter"
    DIGIT = "Must contain at least one digit"
    UNDERSCORE = "Must contain at least one underscore (_)"


def is_valid_password(password: str) -> bool:
    # Check if the password is longer than 8 characters
    if len(password) <= 8:
        return False

    # Check if it contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if it contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if it contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check if it contains at least one underscore
    if "_" not in password:
        return False

    return True


def print_help() -> None:
    click.echo("Password Validation Criteria:")

    for criterion in PasswordCriteria:
        click.echo(f"- {criterion.value}")

    click.echo()


@click.command()
def validate_password() -> None:
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

    password = click.prompt("Enter your password", hide_input=True)
    confirm_password = click.prompt("Confirm your password", hide_input=True)

    click.echo("\nValidating your password...")

    if password == confirm_password and is_valid_password(password):
        # ✅ - 2705
        click.secho(
            "✅ Your password is valid!",
            fg="green",
        )
    else:
        # ❌ - 274C
        click.secho(
            "❌ Your password is invalid. Please ensure it meets all criteria.",
            fg="red",
        )


if __name__ == "__main__":
    validate_password()
