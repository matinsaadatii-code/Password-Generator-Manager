
"""
Helper Functions
================

This module provides utility functions for managing saved passwords
and PIN codes.

It handles JSON file operations, record creation, filtering,
timestamp generation, and displaying saved records.

The data is stored locally in a JSON file. The file path can be
configured through the ``DATA_PATH`` environment variable.

Functions:
    load_items: Load all saved records from the JSON file.
    save_items: Save records to the JSON file.
    now_str: Return the current date and time.
    save_item: Create and save a new record.
    get_items_by_type: Filter records by their generator type.
    print_item: Display the details of a saved record.

Dependencies:
    - json
    - uuid
    - os
    - datetime
    - python-dotenv

.. warning::
    Passwords and PIN codes are currently stored as plain text.
    This implementation is intended for educational purposes and
    should not be used as a production password manager.
"""

import json
import uuid
import os

from datetime import datetime
from typing import Any

from dotenv import load_dotenv


# ============================================================
# DATA CONFIGURATION
# ============================================================

# Load environment variables from the .env file.
load_dotenv()

# Define the path of the JSON database.
# If DATA_PATH is not defined, data.json will be used.
DATA_PATH: str = os.getenv("DATA_PATH", "data.json")


# A saved record is represented as a dictionary with string keys
# and values that may have different data types.
Item = dict[str, Any]


# ============================================================
# JSON FILE OPERATIONS
# ============================================================

def load_items() -> list[Item]:
    """
    Load all saved records from the JSON database.

    The function reads the JSON file and returns its contents
    as a list of records.

    If the file does not exist or contains invalid JSON,
    an empty list is returned.

    :return: A list containing all saved records.
    :rtype: list[Item]

    .. note::
        If the JSON file contains a single dictionary instead
        of a list, the dictionary is wrapped inside a list.

    .. warning::
        Other unexpected JSON root types are treated as empty data.
    """

    try:
        # Open the JSON file using UTF-8 encoding.
        with open(DATA_PATH, "r", encoding="utf-8") as f:

            # Deserialize JSON data into a Python object.
            items: Any = json.load(f)

            # Ensure that the returned data is always a list.
            if isinstance(items, dict):
                items = [items]
            elif not isinstance(items, list):
                items = []

    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty list if the file is missing
        # or contains invalid JSON.
        items = []

    return items


def save_items(items: list[Item]) -> None:
    """
    Save all records to the JSON database.

    The function serializes the provided list of records
    and writes it to the configured JSON file.

    :param items: List of records to be saved.
    :type items: list[Item]
    :return: None
    :rtype: None

    .. note::
        Existing file contents are overwritten.

    .. warning::
        The parent directory of ``DATA_PATH`` must already exist.
    """

    # Open the JSON file in write mode.
    with open(DATA_PATH, "w", encoding="utf-8") as f:

        # Serialize the Python objects into formatted JSON.
        json.dump(
            items,
            f,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# DATE AND TIME UTILITIES
# ============================================================

def now_str() -> str:
    """
    Return the current local date and time as a string.

    The datetime value is formatted using ISO 8601 conventions,
    with a space separating the date and time.

    :return: Current local date and time.
    :rtype: str

    .. example::

        ``2026-11-10 14:30:00``
    """

    return datetime.now().isoformat(sep=" ", timespec="seconds")


# ============================================================
# RECORD MANAGEMENT
# ============================================================

def save_item(name: str, password: str, pass_type: str) -> None:
    """
    Create and save a new password or PIN record.

    A unique identifier is generated for each record using UUID4.

    Each record contains the following fields:

    * ``name``: User-defined name of the record.
    * ``password``: Generated or manually entered password/PIN.
    * ``date``: Record creation date and time.
    * ``type``: Generator category, such as ``rpg`` or ``pin``.
    * ``id``: Unique identifier generated using UUID4.

    :param name: Name assigned to the saved record.
    :type name: str
    :param password: Password or PIN value to be stored.
    :type password: str
    :param pass_type: Category of the generated value.
    :type pass_type: str
    :return: None
    :rtype: None

    .. note::
        Existing records are loaded before the new record is appended.
        The updated list is then saved to the JSON database.
    """

    # Load all existing records.
    items: list[Item] = load_items()

    # Create a new record.
    new_item: Item = {
        "name": name,
        "password": password,
        "date": now_str(),
        "type": pass_type,
        "id": str(uuid.uuid4()),
    }

    # Add the new record to the existing records.
    items.append(new_item)

    # Persist the updated records.
    save_items(items)


def get_items_by_type(pass_type: str) -> list[Item]:
    """
    Retrieve records belonging to a specific generator category.

    The function filters all saved records based on their ``type``
    field.

    :param pass_type: Generator category to filter by.
        For example, ``rpg`` or ``pin``.
    :type pass_type: str

    :return: A list of records matching the specified category.
    :rtype: list[Item]

    .. note::
        The function returns an empty list if no matching records
        are found.
    """

    # Load all records and filter them by their generator type.
    return [
        item
        for item in load_items()
        if item.get("type") == pass_type
    ]


# ============================================================
# RECORD DISPLAY
# ============================================================

def print_item(item: Item) -> None:
    """
    Display the details of a saved password or PIN record.

    The function prints the record's name, password/PIN,
    creation date, optional update date, and unique identifier.

    :param item: Dictionary containing the record information.
    :type item: Item

    :return: None
    :rtype: None

    .. note::
        The ``updated`` field is displayed only if it exists
        in the provided record.

    .. warning::
        This function prints the stored password/PIN in plain text.
    """

    # Print a separator before displaying the record.
    print("-" * 50)

    # Display the main record information.
    print(f'Name: {item["name"]}')
    print(f'Password/PIN: {item["password"]}')
    print(f'Date: {item["date"]}')

    # Display the last update date if the record was modified.
    if item.get("updated"):
        print(f'Updated: {item["updated"]}')

    # Display the unique record identifier.
    print(f'ID: {item["id"]}')

