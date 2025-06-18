# Python Scripts

> A collection of automation scripts written in Python for various tasks.

## Table of Contents

* [Project Overview](#project-overview)
* [Requirements](#requirements)
* [How to Install](#how-to-install)
* [Available Scripts](#available-scripts)
  * [Generate password](#generate-password)
  * [Switch PHP version](#switch-php-version)
  * [Development setup](#development-setup)
  * [Backup files](#backup-files)
* [Contributing](#contributing)
* [License](#license)

## Project Overview

This repository contains Python scripts designed to automate common tasks and improve productivity. Each script is standalone and can be run from the command line.

## Requirements

* Python 3.7+
* pip
* [pyperclip](https://pypi.org/project/pyperclip/) (for clipboard functionality)
* [python-dotenv](https://pypi.org/project/python-dotenv/) (for `.env` support)
* **Linux:** For clipboard support, you may need to install `xclip` or `xsel` (see notes below).

All required Python packages are listed in [`requirements.txt`](requirements.txt).

[⬆ back to top](#table-of-contents)

## How to Install

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd python_scripts
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

**Note:**  
For clipboard support on Linux, you may need to install `xclip` or `xsel`:

```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

[⬆ back to top](#table-of-contents)

## Available Scripts

* [Generate password](#generate-password)
* [Switch PHP version](#switch-php-version)
* [Development setup](#development-setup)
* [Backup files](#backup-files)

---

### Generate password

* **File:** [`src/generate_password.py`](src/generate_password.py)
* **Parameters:** Optional (`-l`, `--length`)
* **Description:** Generate a strong and secure password. The password is automatically copied to your clipboard.

**Notes:**
- **Password length must be at least 8 and divisible by 4** (e.g., 8, 12, 16, 20, ...).
- Uses `pyperclip` to copy the password to your clipboard. On Linux, you may need to install `xclip` or `xsel`.

**Usage:**

```bash
# Show help
python3 src/generate_password.py --help

# Generate password with 20 characters (default)
python3 src/generate_password.py

# Generate password with 16 characters
python3 src/generate_password.py -l 16
```

**Example output:**
```
A7!dQw2@rT9#bL5%
```

[⬆ back to available scripts](#available-scripts)

---

### Switch PHP version

* **File:** [`src/php_switch.py`](src/php_switch.py)
* **Parameters:** Optional (`php_version`)
* **Description:** Switch between installed PHP versions using `update-alternatives`. The script only allows switching to a version that is already installed on your system.

**Requirements:**
- Must be run on a system using `update-alternatives` for PHP (e.g., Debian/Ubuntu).
- Requires `sudo` privileges to switch PHP versions.

**Usage:**

```bash
# Show help
python3 src/php_switch.py --help

# List installed PHP versions and interactively select one
python3 src/php_switch.py

# Switch to a specific PHP version (e.g., 8.3)
python3 src/php_switch.py 8.3
```

**Features:**
- Lists all installed PHP versions.
- Shows the currently set PHP version.
- Prevents switching if the selected version is already set.
- Displays the PHP version after switching.
- Handles user interruptions (`Ctrl+C`, `Ctrl+D`) gracefully.

**Example output:**
```
Installed PHP versions:
1. PHP 8.3 (/usr/bin/php8.3)
2. PHP 8.2 (/usr/bin/php8.2)
Select the PHP version to switch to (by number): 1
Currently set PHP version: /usr/bin/php8.2
✅ Successfully switched to PHP version at /usr/bin/php8.3.
PHP 8.3.7 (cli) (built: Jun  1 2025 12:00:00) ( NTS )
...
```

[⬆ back to available scripts](#available-scripts)

---

### Development setup

* **File:** [`src/dev_setup.py`](src/dev_setup.py)
* **Parameters:** `issue-number` (required), `issue-name` (required)
* **Description:** This script helps set up a new Git branch for a development task based on an issue number and title. It allows you to select a base branch, creates a new branch with a formatted name, checks it out, optionally pushes it to the remote repository, and copies a formatted commit message to the clipboard.

**Environment Variables:**  
You can configure the script using a `.env` file (see `.env.example`):

- `BRANCH_PREFIX` (default: `issues`)
- `REQUEST_PREFIX` (default: `refs:`)
- `ISSUE_BASE_PATH` (used for issue link in the commit message; if set to `https://github.com/<username>`, the script will auto-detect the repo name from the current folder and construct the full repo URL for the issue link)

**Usage:**

```bash
# Show help
python3 src/dev_setup.py --help

# Create and push a new branch for issue 123 with title "Fix login bug"
python3 src/dev_setup.py 123 "Fix login bug"
```

**Features:**
- Checks if you are in a Git repository.
- Lets you select the base branch interactively.
- Creates a new branch with a formatted name.
- Optionally pushes the branch to remote.
- Copies a formatted commit message to your clipboard (requires `pyperclip` and clipboard support).
  - If `ISSUE_BASE_PATH` is set to a GitHub user URL (e.g., `https://github.com/username`), the script will append the current folder name as the repo name and use it for the issue link.
  - If not, only the name is copied (and printed).
- Cleans up if you cancel before pushing.
- Handles user interruptions (`Ctrl+C`, `Ctrl+D`) gracefully.
- Exits with an error if required arguments are missing.

**Example output:**
```
Located in directory: myproject

Available branches:
1. main
2. develop
3. feature/old-task

Select the branch number to create new branch from: 2
Will create branch issues/123_fix_login_bug from develop

Do you wish to proceed? [y/n]: y

Will push local branch to remote
Do you wish to proceed? [y/n]: y

Copied message description to the clipboard:

Based on issues [#123](https://github.com/username/myproject/issues/123)

Copied message name info to the clipboard:

refs: #123 Fix login bug
```

**Note:**  
For clipboard support, you may need to install `xclip` or `xsel` on Linux.

[⬆ back to available scripts](#available-scripts)

---

### Backup files

* **File:** [`src/backup.py`](src/backup.py)
* **Parameters:** None (use `-h` for help)
* **Description:** Backup important files, folders, and environment files from your system to a specified backup location. All paths and backup options are configured via the `.env` file.

**Environment Variables:**  
Configure backup sources and destinations in your `.env` file (see `.env.example`):

- `BACKUP_LOCATION`: Destination directory for backups.
- `SYSTEM_DESTINATION_FOLDER_NAME`: Name for the system backup folder.
- `SYSTEM_SOURCE_PATHS`: Comma-separated list of system files to back up.
- `VSCODE_DESTINATION_FOLDER_NAME`: Name for the VS Code backup folder.
- `VSCODE_SOURCE_PATHS`: Comma-separated list of VS Code settings/snippets to back up.
- `PROJECTS_DESTINATION_FOLDER_NAME`: Name for the projects backup folder.
- `PROJECTS_SOURCE_PATHS`: Comma-separated list of project directories to back up (absolute paths).
- `DEPLOYMENTS_DESTINATION_FOLDER_NAME`: Name for the deployments backup folder.
- `DEPLOYMENT_SOURCE_PATHS`: Comma-separated list of deployment directories to back up (absolute paths).

**Usage:**

```bash
# Show help
python3 src/backup.py -h

# Run backup
python3 src/backup.py
```

**Features:**
- Reads all configuration from `.env` file.
- Backs up system files, VS Code settings, project environment files, and deployment folders.
- For each project in `PROJECTS_SOURCE_PATHS`, backs up `.env` or `.env.rb` if present, and also backs up the `.vscode` folder if it exists.
- Uses `sudo` privileges to create/remove backup directories if needed.
- Handles permission errors gracefully.
- Handles user interruptions (`Ctrl+C`, `Ctrl+D`) gracefully.
- Prints errors for any files or folders that could not be copied.

**Example .env settings:**
```env
BACKUP_LOCATION="/home/your-username/Documents/backup/automated"
SYSTEM_DESTINATION_FOLDER_NAME="system"
SYSTEM_SOURCE_PATHS="/home/your-username/.bashrc,/home/your-username/.gitconfig,/etc/hosts"
VSCODE_DESTINATION_FOLDER_NAME="vscode"
VSCODE_SOURCE_PATHS="/home/your-username/.config/Code/User/settings.json,/home/your-username/.config/Code/User/snippets/global-snippets.code-snippets"
PROJECTS_DESTINATION_FOLDER_NAME="environments"
PROJECTS_SOURCE_PATHS="/var/www/project-one,/var/www/project-two"
DEPLOYMENTS_DESTINATION_FOLDER_NAME="deployments"
DEPLOYMENT_SOURCE_PATHS="/var/www/project-one/deploy,/var/www/project-two/deploy"
```

**Example output:**
```
Completed all backup steps.
```

[⬆ back to available scripts](#available-scripts)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

[⬆ back to top](#table-of-contents)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

[⬆ back to top](#table-of-contents)
