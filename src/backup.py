#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


def parse_env_list(var_name):
    value = os.getenv(var_name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


def get_env_file_for_environment(environment):
    """
    Returns the environment file name for a given environment.
    Uses ENVIRONMENTS_WITH_RB from .env to determine which environments use .env.rb.
    """
    env_with_rb = os.getenv("ENVIRONMENTS_WITH_RB", "")
    rb_envs = [
        item.split(":")[1] for item in env_with_rb.split(",") if item and ":" in item
    ]
    if environment in rb_envs:
        return ".env.rb"
    return ".env"


def end(is_with_error, error_text=None):
    if not is_with_error:
        print(f"Successfully backed up all data.")
        sys.exit(0)
    else:
        print(f"Error: [{error_text}]")
        sys.exit(1)


def sudo_makedirs(path):
    """
    Create directories with sudo privileges if necessary.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except PermissionError:
            # Try with sudo if permission denied
            subprocess.run(["sudo", "mkdir", "-p", path], check=True)


def sudo_rmtree(path):
    """
    Remove directories with sudo privileges if necessary.
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except PermissionError:
            subprocess.run(["sudo", "rm", "-rf", path], check=True)


def copy_directory_contents(source_dir, destination_dir):
    """
    Copies the entire content of a source directory to a new destination.

    Args:
        source_dir (str): The path to the directory whose contents are to be copied.
        destination_dir (str): The path to the new directory where contents will be copied.
                                If this directory already exists, it must be empty.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    try:
        shutil.copytree(source_dir, destination_dir)
    except shutil.Error as e:
        print(f"Error copying directory: {e}")
    except OSError as e:
        print(f"OS Error: {e}")


def prepare_directories():
    # System
    if SYSTEM_PATHS_ON_MACHINE:
        system_dir = os.path.join(BACKUP_LOCATION, SYSTEM_FOLDER)
        sudo_rmtree(system_dir)
        sudo_makedirs(system_dir)
    # VS Code
    if VSCODE_PATHS_ON_MACHINE:
        vscode_dir = os.path.join(BACKUP_LOCATION, VSCODE_FOLDER)
        sudo_rmtree(vscode_dir)
        sudo_makedirs(vscode_dir)
    # Environments
    if ENVIRONMENTS_ON_MACHINE:
        envs_dir = os.path.join(BACKUP_LOCATION, ENVIRONMENTS_FOLDER)
        sudo_rmtree(envs_dir)
        sudo_makedirs(envs_dir)
        for environment in ENVIRONMENTS_ON_MACHINE:
            sudo_makedirs(os.path.join(envs_dir, os.path.basename(environment)))
    # Deployments
    if DEPLOYMENT_FOLDERS_ON_MACHINE:
        deployments_dir = os.path.join(BACKUP_LOCATION, DEPLOYMENTS_FOLDER)
        sudo_rmtree(deployments_dir)
        sudo_makedirs(deployments_dir)
    # Home
    if HOME_PATHS_ON_MACHINE:
        home_dir = os.path.join(BACKUP_LOCATION, HOME_FOLDER)
        sudo_rmtree(home_dir)
        sudo_makedirs(home_dir)


def do_backup():
    # System
    if SYSTEM_PATHS_ON_MACHINE:
        system_dir = os.path.join(BACKUP_LOCATION, SYSTEM_FOLDER)
        for system_path in SYSTEM_PATHS_ON_MACHINE:
            try:
                shutil.copy(system_path, system_dir)
            except Exception as e:
                print(f"Unable to copy {system_path}: {e}")

    # VS Code
    if VSCODE_PATHS_ON_MACHINE:
        vscode_dir = os.path.join(BACKUP_LOCATION, VSCODE_FOLDER)
        for vscode_path in VSCODE_PATHS_ON_MACHINE:
            try:
                shutil.copy(vscode_path, vscode_dir)
            except Exception as e:
                print(f"Unable to copy {vscode_path}: {e}")

    # Environments
    if ENVIRONMENTS_ON_MACHINE:
        envs_dir = os.path.join(BACKUP_LOCATION, ENVIRONMENTS_FOLDER)
        for environment in ENVIRONMENTS_ON_MACHINE:
            env_file = get_env_file_for_environment(environment)
            src_env = os.path.join(LOCALHOST_LOCATION, environment, env_file)
            dst_env = os.path.join(
                envs_dir,
                os.path.basename(environment),
                env_file,
            )
            try:
                sudo_makedirs(os.path.dirname(dst_env))
                shutil.copy(src_env, dst_env)
            except Exception as e:
                print(f"Unable to copy {environment} {env_file}: {e}")

            # Copy .vscode folder if it exists in the environment
            src_vscode = os.path.join(LOCALHOST_LOCATION, environment, ".vscode")
            dst_vscode = os.path.join(
                envs_dir, os.path.basename(environment), ".vscode"
            )
            if os.path.isdir(src_vscode):
                try:
                    # Remove destination if it exists to avoid copytree error
                    if os.path.exists(dst_vscode):
                        shutil.rmtree(dst_vscode)
                    shutil.copytree(src_vscode, dst_vscode)
                except Exception as e:
                    print(f"Unable to copy .vscode folder for {environment}: {e}")

    # Deployments
    if DEPLOYMENT_FOLDERS_ON_MACHINE:
        deployments_dir = os.path.join(BACKUP_LOCATION, DEPLOYMENTS_FOLDER)
        for deployment in DEPLOYMENT_FOLDERS_ON_MACHINE:
            try:
                head1, tail1 = os.path.split(deployment)
                head2, deployment_folder_name = os.path.split(head1)
                copy_directory_contents(
                    deployment,
                    deployments_dir + "/" + deployment_folder_name,
                )
            except Exception as e:
                print(f"Unable to copy {deployment} {env_file}: {e}")

    # Home
    if HOME_PATHS_ON_MACHINE:
        home_dir = os.path.join(BACKUP_LOCATION, HOME_FOLDER)
        for home_path in HOME_PATHS_ON_MACHINE:
            src = os.path.join(HOME_LOCATION, home_path)
            dst = os.path.join(home_dir, os.path.basename(home_path))
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy(src, dst)
            except Exception as e:
                print(f"Unable to copy {home_path}: {e}")


# Environment variables
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")
HOME_LOCATION = os.getenv("HOME_LOCATION")
LOCALHOST_LOCATION = os.getenv("LOCALHOST_LOCATION")
SYSTEM_FOLDER = os.getenv("SYSTEM_FOLDER")
VSCODE_FOLDER = os.getenv("VSCODE_FOLDER")
ENVIRONMENTS_FOLDER = os.getenv("ENVIRONMENTS_FOLDER")
DEPLOYMENTS_FOLDER = os.getenv("DEPLOYMENTS_FOLDER")
HOME_FOLDER = os.getenv("HOME_FOLDER")
SYSTEM_PATHS_ON_MACHINE = parse_env_list("SYSTEM_PATHS_ON_MACHINE")
VSCODE_PATHS_ON_MACHINE = parse_env_list("VSCODE_PATHS_ON_MACHINE")
ENVIRONMENTS_ON_MACHINE = parse_env_list("ENVIRONMENTS_ON_MACHINE")
HOME_PATHS_ON_MACHINE = parse_env_list("HOME_PATHS_ON_MACHINE")
DEPLOYMENT_FOLDERS_ON_MACHINE = parse_env_list("DEPLOYMENT_FOLDERS_ON_MACHINE")


def main():
    parser = argparse.ArgumentParser(description="Backup documents on Linux machine.")
    parser.parse_args()
    prepare_directories()
    do_backup()
    end(False)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nScript canceled. Exiting.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C). Exiting.")
        sys.exit(0)
