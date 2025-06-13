#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

import pyperclip
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BRANCH_PREFIX = os.getenv("BRANCH_PREFIX", "issues")
REQUEST_PREFIX = os.getenv("REQUEST_PREFIX", "refs:")
ISSUE_BASE_PATH = os.getenv("ISSUE_BASE_PATH", "")


def issue_name_for_branch(issue_name):
    """
    Convert issue name to a valid branch name format.
    Args:
        issue_name (str): The name of the issue.
    Returns:
        str: A formatted branch name derived from the issue name.
    """
    name = issue_name.replace(" ", "_").replace("&", "and").replace("|", "-")
    return name.lower()


def is_git_repository():
    """
    Check if the current directory is a git repository.
    Returns:
        bool: True if the current directory is a git repository, False otherwise.
    """
    return os.path.isdir(".git")


def get_current_directory():
    """
    Get the name of the current working directory.
    Returns:
        str: The name of the current working directory.
    """
    return os.path.basename(os.getcwd())


def user_input(message):
    """
    Prompt the user for input with a custom message.
    Args:
        message (str): The message to display to the user.
    Returns:
        str: The input provided by the user.
    """
    return input(f"{message}: ")


def do_you_wish_to_proceed():
    """
    Prompt the user to confirm if they wish to proceed with the operation.
    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        yn = input("Do you wish to proceed? [y/n]: ").strip().lower()
        if yn in ("y", "yes"):
            return True
        elif yn in ("n", "no"):
            return False


def end(is_with_error, error_text=None):
    """
    End the script with a message indicating success or failure.
    Args:
        is_with_error (bool): True if there was an error, False otherwise.
        error_text (str, optional): The error message to display if there was an error.
    """
    if is_with_error:
        print(f"Script finishing with ERROR [{error_text}]")
        sys.exit(1)
    else:
        print("Script finishing OK")
        sys.exit(0)


def show_help(script_name):
    print(f"\nRunning {script_name}")
    print("Description: Development setup for git\n")
    print(f"Show this help  : {script_name} -h")
    print(f"Run this script : {script_name} [issue-number] [issue-name]\n")


def get_git_branches():
    """Return a list of all local git branches."""
    result = subprocess.run(["git", "branch", "--list"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Unable to list git branches.")
        sys.exit(1)
    # Remove the '*' from the current branch and strip whitespace
    branches = [
        line.replace("*", "").strip() for line in result.stdout.strip().split("\n")
    ]
    return [b for b in branches if b]


def select_branch(branches):
    """Prompt user to select a branch from the list."""
    print("Available branches:")
    for idx, branch in enumerate(branches, 1):
        print(f"{idx}. {branch}")
    while True:
        try:
            choice = int(
                user_input("\nSelect the branch number to create new branch from")
            )
            if 1 <= choice <= len(branches):
                return branches[choice - 1]
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    script_name = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(
        description="Development setup for git. Creates a new branch for an issue and pushes it to remote.",
        add_help=False,
        usage=f"{script_name} [issue-number] [issue-name]",
    )
    parser.add_argument("issue_number", nargs="?", help="Issue number (required)")
    parser.add_argument("issue_name", nargs="?", help="Issue name (required)")
    parser.add_argument(
        "-h", "--help", action="store_true", help="Show help message and exit"
    )

    args = parser.parse_args()

    if args.help or not args.issue_number or not args.issue_name:
        show_help(script_name)
        if not args.help:
            print("ERROR: Both issue-number and issue-name are required!\n")
        sys.exit(0 if args.help else 1)

    print(f"Script {script_name} starting...\n")

    print(f"Located in directory: {get_current_directory()}\n")

    if not is_git_repository():
        end(True, "Not git repo")

    branches = get_git_branches()
    source_branch = select_branch(branches)
    target_branch = (
        f"{BRANCH_PREFIX}/{args.issue_number}_{issue_name_for_branch(args.issue_name)}"
    )
    print(f"Will create branch {target_branch} from {source_branch}\n")

    if not do_you_wish_to_proceed():
        end(False)

    # Checkout source branch
    result = subprocess.run(["git", "checkout", source_branch])
    if result.returncode != 0:
        end(True, f"Not able to checkout to the {source_branch}")

    subprocess.run(["git", "pull"])

    # Create and checkout new branch
    subprocess.run(["git", "branch", target_branch])
    subprocess.run(["git", "checkout", target_branch])
    print("\nWill push local branch to remote")

    if do_you_wish_to_proceed():
        subprocess.run(["git", "push", "-u", "origin", target_branch])

        # Create message name and message description
        message_name = (
            f"Name: {REQUEST_PREFIX} #{args.issue_number} {args.issue_name}\n"
        )
        if ISSUE_BASE_PATH:
            message_description = f"Description: Based on {BRANCH_PREFIX} [#{args.issue_number}]({ISSUE_BASE_PATH}/{args.issue_number})"
        else:
            message_description = ""

        # Create message for clipboard
        message_for_clipboard = message_name + message_description

        """
        Copy message to clipboard is best if you have installed https://github.com/diodon-dev/diodon on your system.
        """
        pyperclip.copy(message_description)
        pyperclip.copy(message_name)

        print(f"\nCopied following info to the clipboard:\n\n{message_for_clipboard}")
    else:
        subprocess.run(["git", "checkout", source_branch])
        subprocess.run(["git", "branch", "-D", target_branch])

    end(False)


if __name__ == "__main__":
    main()
