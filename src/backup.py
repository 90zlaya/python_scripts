#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


def get_env(var_name, is_list=False):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(
            f"Error: Required environment variable '{var_name}' is not set."
        )
    if is_list:
        value = os.getenv(var_name, "")
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


def get_parent_folder_name(path):
    head1, tail1 = os.path.split(path)
    head2, parent_folder_name = os.path.split(head1)
    return parent_folder_name


def sudo_makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except PermissionError:
            # Try with sudo if permission denied
            subprocess.run(["sudo", "mkdir", "-p", path], check=True)


def sudo_rmtree(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except PermissionError:
            subprocess.run(["sudo", "rm", "-rf", path], check=True)


def do_simple_backup(backup_destination, env_prefixes):
    for env_prefix in env_prefixes:
        src_paths = get_env(f"{env_prefix}_SOURCE_PATHS", True)
        if src_paths:
            dest_folder_name = os.getenv(f"{env_prefix}_DESTINATION_FOLDER_NAME")
            # Delete old destination folder (with files) and create new
            dest_path = os.path.join(str(backup_destination), str(dest_folder_name))
            sudo_rmtree(dest_path)
            sudo_makedirs(dest_path)
            # Backup destination path
            for src_path in src_paths:
                try:
                    shutil.copy(src_path, dest_path)
                except Exception as e:
                    print(
                        f"Error in {dest_folder_name} backup: Unable to copy {dest_path}: {e}"
                    )


def do_projects_backup(backup_location):
    # Projects environment variables
    projects_destination_folder = get_env("PROJECTS_DESTINATION_FOLDER_NAME")
    projects_source_paths = get_env("PROJECTS_SOURCE_PATHS", True)
    # Check if there are defined projects for backup
    if projects_source_paths:

        def get_env_file_for_environment(project):
            if os.path.isfile(f"{project}/.env"):
                return ".env"
            elif os.path.isfile(f"{project}/.env.rb"):
                return ".env.rb"
            else:
                return ""

        def is_subfolder_of_project(project_path):
            return os.path.basename(project_path) in ["api", "frontend", "backend"]

        def get_project_name(project_path):
            folder_name = os.path.basename(project_path)
            if is_subfolder_of_project(project_path):
                parent_folder_name = get_parent_folder_name(project_path)
                return parent_folder_name + "/" + folder_name
            return folder_name

        # Delete old projects destination folder (with files) and create new
        projects_dir = os.path.join(backup_location, str(projects_destination_folder))
        sudo_rmtree(projects_dir)
        sudo_makedirs(projects_dir)
        for project in projects_source_paths:
            sudo_makedirs(os.path.join(projects_dir, get_project_name(project)))
        # Projects backup
        for project in projects_source_paths:
            env_file = get_env_file_for_environment(project)
            if env_file:
                src_env = os.path.join(project, env_file)
                dst_env = os.path.join(
                    projects_dir,
                    get_project_name(project),
                    env_file,
                )
                try:
                    sudo_makedirs(os.path.dirname(dst_env))
                    shutil.copy(src_env, dst_env)
                except Exception as e:
                    print(f"Unable to backup {project} {env_file}: {e}")

            # Copy .vscode folder if it exists in the project
            project_path = (
                os.path.dirname(project)
                if is_subfolder_of_project(project)
                else project
            )
            project_name = (
                get_parent_folder_name(project)
                if is_subfolder_of_project(project)
                else os.path.basename(project)
            )
            src_vscode = os.path.join(project_path, ".vscode")
            dst_vscode = os.path.join(projects_dir, project_name, ".vscode")
            if os.path.isdir(src_vscode):
                try:
                    # Remove destination if it exists to avoid copytree error
                    if os.path.exists(dst_vscode):
                        shutil.rmtree(dst_vscode)
                    shutil.copytree(src_vscode, dst_vscode)
                except Exception as e:
                    print(f"Unable to backup .vscode folder for {project}: {e}")


def do_deployments_backup(backup_location):
    # Deployments environment variables
    deployments_destination_folder_name = get_env("DEPLOYMENTS_DESTINATION_FOLDER_NAME")
    deployment_source_paths = get_env("DEPLOYMENT_SOURCE_PATHS", True)
    # Check if there are defined deployments for backup
    if deployment_source_paths:

        def copy_directory_contents(source_dir, destination_dir):
            if not os.path.exists(source_dir):
                print(
                    f"Error copying directory contents: Source directory '{source_dir}' does not exist."
                )
                return

            try:
                shutil.copytree(source_dir, destination_dir)
            except shutil.Error as e:
                print(f"Error copying directory: {e}")
            except OSError as e:
                print(f"OS Error: {e}")

        # Delete old deployments destination folder (with files) and create new
        deployments_dir = os.path.join(
            backup_location, str(deployments_destination_folder_name)
        )
        sudo_rmtree(deployments_dir)
        sudo_makedirs(deployments_dir)
        # Deployments backup
        deployments_dir = os.path.join(
            backup_location, str(deployments_destination_folder_name)
        )
        for deployment in deployment_source_paths:
            try:
                copy_directory_contents(
                    deployment,
                    deployments_dir + "/" + get_parent_folder_name(deployment),
                )
            except Exception as e:
                print(f"Unable to backup deployment {deployment}: {e}")


if __name__ == "__main__":
    try:
        # Defining argument parser
        parser = argparse.ArgumentParser(
            description="Backup documents on Linux machine."
        )
        parser.parse_args()
        # Loading environment variables
        backup_location = get_env("BACKUP_LOCATION")
        # Do backups
        do_simple_backup(backup_location, ["SYSTEM", "VSCODE"])
        do_projects_backup(backup_location)
        do_deployments_backup(backup_location)
        # Display message
        print(f"Completed all backup steps.")
    except EOFError:
        print("\nScript canceled. Exiting.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C). Exiting.")
        sys.exit(0)
