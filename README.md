# Password Validation CLI Tool

This is a Python-based CLI (Command-Line Interface) tool for validating passwords against specific criteria. The tool provides instant feedback on whether the entered password is valid or not and includes tests to ensure robust functionality.

---

## Features

- Validate passwords interactively via CLI.
- Ensures the following password criteria are met:
  - More than 8 characters long.
  - At least one uppercase letter.
  - At least one lowercase letter.
  - At least one digit.
  - At least one underscore (`_`).
- Includes tests to validate functionality using `pytest`.
- Clear and color-coded feedback for user experience.

---

## Requirements

- Python 3.8 or higher
- `pip` for package management

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/espedzhev/password_validation_task
   cd password_validation_task
   
2. Create and activate a virtual environment:
   python3 -m venv .venv 
   source .venv/bin/activate

3. Install the required dependencies
   pip install -r requirements.txt

4. For API
   npm install
   npm run build:ts

# Usage
## Cli

```bash
python app/cli.py
```

## Example Workflow

```bash
Password Validation Criteria:
- Must be more than 8 characters long
- Must contain at least one uppercase letter
- Must contain at least one lowercase letter
- Must contain at least one digit
- Must contain at least one underscore (_)

Enter your password: ********
Confirm your password: ********

Validating your password...
✅ Your password is valid!
```

## Testing
```bash
pytest
```

## Example Test Output
```bash
============================= test session starts ==============================
platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
rootdir: /path/to/project
collected 11 items

app/tests/test_api.py ...                                              [ 21%]
app/tests/test_cli.py ....                                             [ 50%]
app/tests/test_validation.py .......                                   [100%]

============================== 14 passed in 0.36s  ===============================

```

## API
```bash
uvicorn app.main:app
```
- http://127.0.0.1:8000 webinterface
- http://127.0.0.1:8000/docs swagger ui
