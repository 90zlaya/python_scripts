#!/usr/bin/env python3

import argparse
import random
import string

import pyperclip

MINIMUM_LENGTH = 8
NUMBER_OF_CHUNKS = 4


def generate_password(length=20):
    """
    Generate a secure password with the specified length.
    :param length: Length of the password (default is 20)
    :return: A secure password as a string
    """

    if length < MINIMUM_LENGTH:
        raise Exception(
            f"Please enter length greater than or equal to {MINIMUM_LENGTH}."
        )
    if length % NUMBER_OF_CHUNKS != 0:
        raise Exception(
            f"Please enter length divisible by {NUMBER_OF_CHUNKS} like: 8, 12, 16, 20, 24, 28, 32..."
        )

    chunks = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]
    random.shuffle(chunks)

    password = ""
    for chunk in chunks:
        password += "".join(random.sample(chunk, (length // 4)))

    return password


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Generate strong and secure password. Minimum length is {MINIMUM_LENGTH} and must be divisible by {NUMBER_OF_CHUNKS}."
    )
    parser.add_argument(
        "-l", "--length", type=int, default=20, help="Length of the password"
    )

    args = parser.parse_args()

    try:
        password = generate_password(args.length)

        # Copy to clipboard
        pyperclip.copy(password)

        print(password)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
