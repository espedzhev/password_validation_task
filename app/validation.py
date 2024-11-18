def is_valid_password(password: str, rules: dict = None) -> bool:
    rules = rules or {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digit": True,
        "require_underscore": True,
    }

    if len(password) < rules["min_length"]:
        return False

    if rules["require_uppercase"] and not any(char.isupper() for char in password):
        return False

    if rules["require_lowercase"] and not any(char.islower() for char in password):
        return False

    if rules["require_digit"] and not any(char.isdigit() for char in password):
        return False

    if rules["require_underscore"] and "_" not in password:
        return False

    return True
