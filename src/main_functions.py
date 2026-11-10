
"""
Record Management Functions
===========================

This module provides functions for managing saved passwords and PIN codes.

It handles searching, listing, selecting, editing, updating, and deleting
records stored in the JSON database.

The actual file operations are delegated to the :mod:`helpers` module.

Functions:
    search_items: Search records by name, ID, or password/PIN.
    list_items: Display all records belonging to a category.
    pick_item: Allow the user to select a record.
    update_item: Update an existing record.
    edit_item: Modify a selected record.
    delete_item: Delete a selected record.

Dependencies:
    - helpers
    - collections.abc
    - typing

.. note::
    This module provides the application-level logic for record management.
    JSON file operations are implemented separately in ``helpers.py``.
"""

import helpers

from collections.abc import Callable
from typing import Any


# ============================================================
# TYPE DEFINITIONS
# ============================================================

# Define the structure used for saved password/PIN records.
Item = dict[str, Any]


# ============================================================
# SEARCH OPERATIONS
# ============================================================

def search_items(pass_type: str) -> None:
    """
    Search saved records using different search criteria.

    Users can search records by:
        - Name: Partial, case-insensitive name matching.
        - ID: Exact UUID matching.
        - Password/PIN: Exact value matching.

    Only records belonging to the specified generator category
    are included in the search.

    :param pass_type: Generator category to search.
        For example, ``rpg`` or ``pin``.
    :type pass_type: str

    :return: None
    :rtype: None

    .. note::
        Matching records are displayed using
        :func:`helpers.print_item`.

    .. warning::
        Searching by password/PIN requires entering the exact value.
    """

    # Available search methods.
    options: list[str] = [
        "Search by Name",
        "Search by Id",
        "Search by Password/Pin",
        "Back"
    ]

    # Display search menu.
    print("==Search Options==")

    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    print("-" * 50)

    # Get the user's selected search method.
    choice: str = input("Enter your Choice: ").strip()

    # Retrieve records belonging to the requested category.
    items: list[Item] = helpers.get_items_by_type(pass_type)

    # Search records by name.
    if choice == "1":
        query: str = input("Enter the name: ").strip().lower()

        results: list[Item] = [
            item for item in items
            if query in item["name"].lower()
        ]

    # Search records by unique identifier.
    elif choice == "2":
        query = input("Enter the id: ").strip()

        results = [
            item for item in items
            if item["id"] == query
        ]

    # Search records by exact password or PIN value.
    elif choice == "3":
        query = input("Enter the Password/Pin: ")

        results = [
            item for item in items
            if item["password"] == query
        ]

    # Return to the previous menu.
    elif choice == "4":
        return

    # Handle invalid menu selections.
    else:
        print("Please enter correct Choice.")
        return

    # Check whether any matching records were found.
    if not results:
        print("Not found.")
        return

    # Display the number of matching records.
    print(f"Found {len(results)} item(s)!")

    # Display the details of each matching record.
    for item in results:
        helpers.print_item(item)


# ============================================================
# LIST OPERATIONS
# ============================================================

def list_items(pass_type: str) -> list[Item]:
    """
    Retrieve and display all saved records of a specific category.

    Records are displayed with their name, password/PIN, and creation date.

    :param pass_type: Generator category to retrieve.
        For example, ``rpg`` or ``pin``.
    :type pass_type: str

    :return: A list containing all matching records.
        Returns an empty list if no records exist.
    :rtype: list[Item]

    .. note::
        The returned list can be used by other functions,
        such as :func:`pick_item`, to select a specific record.
    """

    # Retrieve all records belonging to the specified category.
    items: list[Item] = helpers.get_items_by_type(pass_type)

    # Handle the case where no records are available.
    if not items:
        print("There are no saved items yet.")
        return items

    # Display the total number of saved records.
    print(f"==Saved items ({len(items)})==")

    # Display a summary of each record.
    for i, item in enumerate(items, start=1):
        print(
            f'{i}. {item["name"]} | '
            f'{item["password"]} | {item["date"]}'
        )

    print("-" * 50)

    return items


# ============================================================
# RECORD SELECTION
# ============================================================

def pick_item(pass_type: str, action: str) -> Item | None:
    """
    Allow the user to select a record from a displayed list.

    The function first displays all records of the requested category.
    The user can then select a record using its list position.

    Pressing Enter without entering a value cancels the selection.

    :param pass_type: Generator category from which a record is selected.
    :type pass_type: str

    :param action: Name of the action being performed.
        For example, ``edit`` or ``delete``.
    :type action: str

    :return: The selected record, or ``None`` if the selection
        is cancelled, invalid, or no records are available.
    :rtype: Item or None

    .. note::
        The selection is based on the displayed list position,
        not the record's unique ID.
    """

    # Display records and retrieve them as a list.
    items: list[Item] = list_items(pass_type)

    # Stop if there are no records to select.
    if not items:
        return None

    # Ask the user to select a record.
    choice: str = input(
        f"Enter the number of the item you want to {action} "
        "(Enter to cancel): "
    ).strip()

    # Allow the user to cancel the operation.
    if not choice:
        return None

    # Validate the entered number.
    if not choice.isdigit() or not 1 <= int(choice) <= len(items):
        print("Please enter a correct Number.")
        return None

    # Convert the one-based menu position to a zero-based list index.
    return items[int(choice) - 1]


# ============================================================
# UPDATE OPERATIONS
# ============================================================

def update_item(item_id: str, **changes: Any) -> bool:
    """
    Update an existing record using its unique identifier.

    The function searches the JSON database for a record matching
    the provided ID and applies the requested changes.

    The ``updated`` field is automatically refreshed whenever
    a record is successfully modified.

    :param item_id: Unique identifier of the record to update.
    :type item_id: str

    :param changes: Keyword arguments containing the fields
        and their new values.
    :type changes: Any

    :return: ``True`` if the record was found and updated;
        otherwise ``False``.
    :rtype: bool

    .. example::

        Update a record's name::

            update_item(
                "record-uuid",
                name="New Password Name"
            )

        Update its password::

            update_item(
                "record-uuid",
                password="new-password"
            )

    .. note::
        The function updates the record's modification timestamp
        using :func:`helpers.now_str`.
    """

    # Load all records from the JSON database.
    items: list[Item] = helpers.load_items()

    # Find the record using its unique identifier.
    for item in items:

        if item.get("id") == item_id:

            # Apply the requested changes to the record.
            item.update(changes)

            # Update the modification timestamp.
            item["updated"] = helpers.now_str()

            # Save the modified records.
            helpers.save_items(items)

            return True

    # Return False if no matching record was found.
    return False


# ============================================================
# EDIT OPERATIONS
# ============================================================

def edit_item(pass_type: str, generate: Callable[[], str]) -> None:
    """
    Edit an existing password or PIN record.

    The user can choose one of the following operations:

        1. Change the record's name.
        2. Manually change its password/PIN.
        3. Generate a new password/PIN automatically.
        4. Cancel the editing operation.

    :param pass_type: Generator category of the record to edit.
        For example, ``rpg`` or ``pin``.
    :type pass_type: str

    :param generate: A callable that generates a new password or PIN.
        It must accept no arguments and return a string.
    :type generate: Callable[[], str]

    :return: None
    :rtype: None

    .. note::
        The ``generate`` argument allows this function to work
        with different generator classes without depending on
        their specific implementations.

    .. seealso::
        :func:`update_item`
        :func:`pick_item`
    """

    # Let the user select a record for editing.
    item: Item | None = pick_item(pass_type, "edit")

    # Stop if no record was selected.
    if item is None:
        return

    # Display the selected record.
    print("You are editing:")
    helpers.print_item(item)

    # Available editing operations.
    options: list[str] = [
        "Change name",
        "Change password/pin manually",
        "Generate a new one",
        "Cancel"
    ]

    # Display the editing menu.
    print("==Edit Options==")

    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    print("-" * 50)

    # Get the user's selected editing operation.
    choice: str = input("Enter your Choice: ").strip()

    # Change the record's name.
    if choice == "1":

        new_name: str = input("Enter the new name: ").strip()

        # Prevent empty record names.
        if not new_name:
            print("Name can't be empty.")
            return

        update_item(item["id"], name=new_name)

    # Manually change the password or PIN.
    elif choice == "2":

        new_password: str = input("Enter the new password/pin: ")

        # Prevent empty password/PIN values.
        if not new_password:
            print("Value can't be empty.")
            return

        update_item(item["id"], password=new_password)

    # Generate a replacement password or PIN.
    elif choice == "3":

        new_password: str = generate()

        update_item(item["id"], password=new_password)

        # Display the newly generated value.
        print(f"New value: {new_password}")

    # Cancel the editing operation if the selection is invalid
    # or the user chooses the cancel option.
    else:
        print("Edit cancelled.")
        return

    print("Item updated successfully!")


# ============================================================
# DELETE OPERATIONS
# ============================================================

def delete_item(pass_type: str) -> None:
    """
    Delete a saved password or PIN record.

    The user first selects a record and then confirms the deletion.
    If confirmation is successful, the record is removed from
    the JSON database.

    :param pass_type: Generator category of the record to delete.
        For example, ``rpg`` or ``pin``.
    :type pass_type: str

    :return: None
    :rtype: None

    .. warning::
        Deletion is permanent in the current implementation.
        The deleted record is not moved to a backup or recycle bin.

    .. note::
        The record is identified by its unique ID rather than
        its position in the list.
    """

    # Let the user select a record for deletion.
    item: Item | None = pick_item(pass_type, "delete")

    # Stop if no record was selected.
    if item is None:
        return

    # Display the selected record before deletion.
    helpers.print_item(item)

    # Ask the user to confirm the deletion.
    confirm: str = input(
        "Are you sure you want to delete this item? (yes, no) "
    ).strip().lower()

    # Cancel deletion unless the user explicitly confirms.
    if confirm != "yes":
        print("Delete cancelled.")
        return

    # Load all records and exclude the selected record.
    items: list[Item] = [
        saved_item
        for saved_item in helpers.load_items()
        if saved_item.get("id") != item["id"]
    ]

    # Save the remaining records to the JSON database.
    helpers.save_items(items)

    print("Item deleted successfully!")
