
"""
Password Generator Application
==============================

This module provides the main command-line interface (CLI) for the
Password Generator application.

Users can interact with the application through different menus
to generate, save, search, list, edit, and delete passwords and PIN codes.

Available generators:
    * Random Password Generator (RPG)
    * Memorable Password Generator (MPG) - Under construction.
    * PIN Code Generator (PCG)

The application delegates password generation to :mod:`pass_classes`,
data persistence to :mod:`helpers`, and record management operations
to :mod:`main_functions`.

Main Features:
    * Generate random passwords.
    * Generate numeric PIN codes.
    * Configure password and PIN lengths.
    * Enable numbers and symbols in random passwords.
    * Save generated values.
    * Search and display saved records.
    * Edit and delete existing records.

Modules:
    :mod:`pass_classes`: Password and PIN generator classes.
    :mod:`helpers`: JSON database and utility functions.
    :mod:`main_functions`: Record management operations.

Execution:
    Run this module directly to start the application.

    .. code-block:: console

        python main.py

.. note::
    The Memorable Password Generator is currently under development.
"""

import pass_classes
import helpers
import main_functions


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    # Main application loop.
    # Keeps displaying the main menu until the user exits.
    while True:

        # Available application features and their abbreviations.
        choices: dict[str, str] = {
            "Random Password Generator": "RPG",
            "Memorable Password Generator": "MPG",
            "Pin Code Generator": "PCG",
            "Exit": ""
        }

        # Display the main menu.
        print("==Password Generator==")

        for i, (choice, abbr) in enumerate(choices.items(), start=1):
            print(f"{i}. {choice} ({abbr})")

        print("-" * 50)

        # Get the user's main menu selection.
        user_choice: str = input("Enter your Choice: ").strip()


        # ====================================================
        # RANDOM PASSWORD GENERATOR MENU
        # ====================================================

        if user_choice == "1":

            # Create a new random password generator instance.
            rpg: pass_classes.RandomPasswordGenerator = (
                pass_classes.RandomPasswordGenerator()
            )

            # Generate the initial password.
            password: str = rpg.generate()

            # Available operations for the Random Password Generator.
            random_password_generator_choices: list[str] = [
                "Include Numbers",
                "Include Symbols",
                "Length",
                "Just give me the RPG",
                "Save this RPG",
                "Search Passwords",
                "List Passwords",
                "Edit a Password",
                "Delete a Password",
                "Exit"
            ]

            # Random Password Generator menu loop.
            while True:

                # Display RPG options.
                print("==RPG Options==")

                for i, choice in enumerate(
                    random_password_generator_choices,
                    start=1
                ):
                    print(f"{i}. {choice}")

                print("-" * 50)

                # Get the user's RPG menu selection.
                random_password_generator_choice: str = input(
                    "Enter your Choice: "
                ).strip()


                # --------------------------------------------
                # Enable Numbers
                # --------------------------------------------

                if random_password_generator_choice == "1":

                    # Include numeric characters in future passwords.
                    rpg.include_numbers = True

                    # Generate a new password using the updated settings.
                    password = rpg.generate()


                # --------------------------------------------
                # Enable Symbols
                # --------------------------------------------

                elif random_password_generator_choice == "2":

                    # Include punctuation characters in future passwords.
                    rpg.include_symbols = True

                    # Generate a new password using the updated settings.
                    password = rpg.generate()


                # --------------------------------------------
                # Change Password Length
                # --------------------------------------------

                elif random_password_generator_choice == "3":

                    # Ask the user for the desired password length.
                    try:
                        new_length: int = int(
                            input("Enter your Length: ")
                        )

                        # Password length must be a positive integer.
                        if new_length < 1:
                            raise ValueError

                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    # Update the generator configuration.
                    rpg.length = new_length

                    # Generate a password with the new length.
                    password = rpg.generate()


                # --------------------------------------------
                # Display Current Password
                # --------------------------------------------

                elif random_password_generator_choice == "4":

                    print(f"Here is your RPG: {password}")
                    continue


                # --------------------------------------------
                # Save Password
                # --------------------------------------------

                elif random_password_generator_choice == "5":

                    # Check whether a password has been generated.
                    if password:

                        # Get a user-defined name for the password.
                        name: str = input(
                            "Enter a name for your Password: "
                        ).strip()

                        if not name:
                            print("Name can't be empty.")
                            continue

                        # Save the password in the JSON database.
                        helpers.save_item(name, password, "rpg")

                        print("Password saved successfully!")

                    else:
                        print(
                            "There is no Password. "
                            "Please create one first."
                        )
                        continue


                # --------------------------------------------
                # Search Saved Passwords
                # --------------------------------------------

                elif random_password_generator_choice == "6":

                    # Search only records belonging to the RPG category.
                    main_functions.search_items("rpg")
                    continue


                # --------------------------------------------
                # List Saved Passwords
                # --------------------------------------------

                elif random_password_generator_choice == "7":

                    # Display all saved RPG records.
                    main_functions.list_items("rpg")
                    continue


                # --------------------------------------------
                # Edit a Saved Password
                # --------------------------------------------

                elif random_password_generator_choice == "8":

                    # Pass the generator method as a callable.
                    # It allows edit_item() to generate a replacement password.
                    main_functions.edit_item("rpg", rpg.generate)
                    continue


                # --------------------------------------------
                # Delete a Saved Password
                # --------------------------------------------

                elif random_password_generator_choice == "9":

                    # Delete a selected RPG record.
                    main_functions.delete_item("rpg")
                    continue


                # --------------------------------------------
                # Exit RPG Menu
                # --------------------------------------------

                elif random_password_generator_choice == "10":

                    break


                # --------------------------------------------
                # Invalid Selection
                # --------------------------------------------

                else:
                    print("Please enter correct Choice.")
                    continue


                # Display the current generated password.
                print(f"Here is your RPG: {password}")

                # Ask whether the user wants to leave the RPG menu.
                user_quit_request: str = input(
                    "You want to quit? (yes, no) "
                ).strip().lower()

                if user_quit_request == "yes":
                    break

                elif user_quit_request == "no":
                    continue


        # ====================================================
        # MEMORABLE PASSWORD GENERATOR
        # ====================================================

        elif user_choice == "2":

            # This feature has not been implemented yet.
            print("Under construction. Please try again later.")

            print("-" * 50)
            continue


        # ====================================================
        # PIN CODE GENERATOR MENU
        # ====================================================

        elif user_choice == "3":

            # Create a new PIN code generator instance.
            pcg: pass_classes.PinCodeGenerator = (
                pass_classes.PinCodeGenerator()
            )

            # Generate the initial PIN.
            pin: str = pcg.generate()

            # Available operations for the PIN Code Generator.
            pin_code_generator_choices: list[str] = [
                "Length",
                "Just Give me the Pin",
                "Save this Pin",
                "Search Pins",
                "List Pins",
                "Edit a Pin",
                "Delete a Pin",
                "Exit"
            ]

            # PIN Code Generator menu loop.
            while True:

                # Display PCG options.
                print("==PCG Options==")

                for i, choice in enumerate(
                    pin_code_generator_choices,
                    start=1
                ):
                    print(f"{i}. {choice}")

                print("-" * 50)

                # Get the user's PCG menu selection.
                pin_code_generator_choice: str = input(
                    "Enter your Choice: "
                ).strip()


                # --------------------------------------------
                # Change PIN Length
                # --------------------------------------------

                if pin_code_generator_choice == "1":

                    # Ask the user for the desired PIN length.
                    try:
                        new_length: int = int(
                            input("Enter your Length: ")
                        )

                        # PIN length must be a positive integer.
                        if new_length < 1:
                            raise ValueError

                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    # Update the generator configuration.
                    pcg.length = new_length

                    # Generate a PIN with the new length.
                    pin = pcg.generate()


                # --------------------------------------------
                # Display Current PIN
                # --------------------------------------------

                elif pin_code_generator_choice == "2":

                    print(f"Here is your Pin: {pin}")
                    continue


                # --------------------------------------------
                # Save PIN
                # --------------------------------------------

                elif pin_code_generator_choice == "3":

                    # Check whether a PIN has been generated.
                    if pin:

                        # Get a user-defined name for the PIN.
                        name: str = input(
                            "Enter a name for your Pin: "
                        ).strip()

                        if not name:
                            print("Name can't be empty.")
                            continue

                        # Save the PIN in the JSON database.
                        helpers.save_item(name, pin, "pin")

                        print("Pin saved successfully!")

                    else:
                        print(
                            "There is no Pin. "
                            "Please create one first."
                        )
                        continue


                # --------------------------------------------
                # Search Saved PINs
                # --------------------------------------------

                elif pin_code_generator_choice == "4":

                    # Search only records belonging to the PIN category.
                    main_functions.search_items("pin")
                    continue


                # --------------------------------------------
                # List Saved PINs
                # --------------------------------------------

                elif pin_code_generator_choice == "5":

                    # Display all saved PIN records.
                    main_functions.list_items("pin")
                    continue


                # --------------------------------------------
                # Edit a Saved PIN
                # --------------------------------------------

                elif pin_code_generator_choice == "6":

                    # Pass the generator method as a callable.
                    # It allows edit_item() to generate a replacement PIN.
                    main_functions.edit_item("pin", pcg.generate)
                    continue


                # --------------------------------------------
                # Delete a Saved PIN
                # --------------------------------------------

                elif pin_code_generator_choice == "7":

                    # Delete a selected PIN record.
                    main_functions.delete_item("pin")
                    continue


                # --------------------------------------------
                # Exit PCG Menu
                # --------------------------------------------

                elif pin_code_generator_choice == "8":

                    break


                # --------------------------------------------
                # Invalid Selection
                # --------------------------------------------

                else:
                    print("Please enter correct Choice.")
                    continue


                # Display the current generated PIN.
                print(f"Here is your Pin: {pin}")

                # Ask whether the user wants to leave the PCG menu.
                user_quit_request: str = input(
                    "You want to quit? (yes, no) "
                ).strip().lower()

                if user_quit_request == "yes":
                    break

                elif user_quit_request == "no":
                    continue


        # ====================================================
        # EXIT APPLICATION
        # ====================================================

        elif user_choice == "4":

            # Display the exit message and terminate the main loop.
            print("Bye!")
            break


        # ====================================================
        # INVALID MAIN MENU SELECTION
        # ====================================================

        else:

            # Handle invalid main menu input.
            print("Please enter correct Choice.")
