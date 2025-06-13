#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys


def get_installed_php_versions():
    """
    Get a list of installed PHP versions using update-alternatives.
    Returns:
        list: A list of paths to the installed PHP versions.
    """
    result = subprocess.run(
        ["update-alternatives", "--list", "php"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error: Could not list PHP versions.")
        return []
    return result.stdout.strip().split("\n")


def extract_version_from_path(php_path):
    """
    Extract the PHP version from the given path.
    Args:
        php_path (str): The path to the PHP executable.
    Returns:
        str: The extracted PHP version, or None if not found.
    """
    # Try to extract version like 8.3, 8.2, 7.4, etc.
    match = re.search(r"php(?:/|)(\d+\.\d+)", php_path)
    if match:
        return match.group(1)
    # Fallback: try to extract from filename
    match = re.search(r"php(\d+\.\d+)", php_path)
    if match:
        return match.group(1)
    return None


def build_version_map(php_paths):
    """
    Build a mapping of PHP versions to their paths.
    Args:
        php_paths (list): A list of paths to the installed PHP versions.
    Returns:
        dict: A dictionary mapping PHP versions to their paths.
    """
    version_map = {}
    for path in php_paths:
        version = extract_version_from_path(path)
        if version:
            version_map[version] = path
    return version_map


def switch_php_version(php_path):
    """
    Switch the PHP version using update-alternatives.
    Args:
        php_path (str): The path to the PHP executable to switch to.
    """
    result = subprocess.run(
        ["sudo", "update-alternatives", "--set", "php", php_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: Could not switch to PHP version at {php_path}.")
        print(result.stderr)
    else:
        print(f"✅ Successfully switched to PHP version at {php_path}.")


def main():
    parser = argparse.ArgumentParser(
        description="Switch between installed PHP versions using update-alternatives. The script will only allow switching to a version that is already installed on your system."
    )
    parser.add_argument(
        "php_version",
        nargs="?",
        help="PHP version to switch to (e.g., 8.3, 8.2, 7.4). Must be one of the installed alternatives.",
    )
    args = parser.parse_args()

    php_paths = get_installed_php_versions()
    if not php_paths:
        print("No PHP versions found.")
        sys.exit(1)

    version_map = build_version_map(php_paths)

    if args.php_version:
        if args.php_version not in version_map:
            print(
                f"Error: PHP version {args.php_version} is not among the installed alternatives."
            )
            print("Installed PHP versions:")
            for v in sorted(version_map):
                print(f"- {v} ({version_map[v]})")
            sys.exit(1)
        switch_php_version(version_map[args.php_version])
    else:
        print("Installed PHP versions:")
        for i, (v, path) in enumerate(sorted(version_map.items()), 1):
            print(f"{i}. PHP {v} ({path})")

        try:
            choice = int(input("Select the PHP version to switch to (by number): "))
            versions = list(sorted(version_map.items()))
            if 1 <= choice <= len(versions):
                switch_php_version(versions[choice - 1][1])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
