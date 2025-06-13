# Python Scripts

> A collection of automation scripts written in Python for various tasks.

## Table of Contents

* [Project Overview](#project-overview)
* [Requirements](#requirements)
* [How to Install](#how-to-install)
* [Available Scripts](#available-scripts)
* [Contributing](#contributing)
* [License](#license)

## Project Overview

This repository contains Python scripts designed to automate common tasks and improve productivity.

## Requirements

* Python 3.7+
* pip

[⬆ back to top](#table-of-contents)

## How to Install

1. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   ```

2. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

[⬆ back to top](#table-of-contents)

## Available Scripts

* [Generate password](#generate-password)
* [Switch PHP version](#switch-php-version)
* [Development setup](#development-setup)

### Generate password

* **File:** [`src/generate_password.py`](src/generate_password.py)
* **Parameters:** Optional
* **Description:** Generate a strong and secure password.

```bash
# Show help
python src/generate_password.py --help

# Generate password with 20 characters
python src/generate_password.py -l 20
```

[⬆ back to available scripts](#available-scripts)

### Switch PHP version

* **File:** [`src/php_switch.py`](src/php_switch.py)
* **Parameters:** Optional
* **Description:** Switch between installed PHP versions using `update-alternatives`. The script will only allow switching to a version that is already installed on your system.

```bash
# Show help
python src/php_switch.py --help

# List installed PHP versions and interactively select one
python src/php_switch.py

# Switch to a specific PHP version (e.g., 8.3)
python src/php_switch.py 8.3
```

[⬆ back to available scripts](#available-scripts)

### Development setup

* **File:** [`src/dev_setup.py`](src/dev_setup.py)
* **Parameters:** `issue-number` (required), `issue-name` (required)
* **Description:** This script helps set up a new Git branch for a development task based on an issue number and title. It allows you to select a base branch, creates a new branch with a formatted name, checks it out, optionally pushes it to the remote repository, and copies a formatted commit message to the clipboard.

```bash
# Show help
python dev_setup.py --help

# Create and push a new branch for issue 123 with title "Fix login bug"
python dev_setup.py 123 "Fix login bug"
```

The script requires a Git repository and optionally reads values from a `.env` file:

* `BRANCH_PREFIX` (default: `issues`)
* `REQUEST_PREFIX` (default: `refs:`)
* `ISSUE_BASE_PATH` (used for issue link in the commit message)

[⬆ back to available scripts](#available-scripts)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

[⬆ back to top](#table-of-contents)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

[⬆ back to top](#table-of-contents)
