
"""
Password Generator Application
==============================

This module provides the main command-line interface (CLI) for the
Password Generator application.

Users interact with the application through a set of menus to generate,
save, search, list, edit, and delete passwords, PIN codes, and JWT
secrets. Each generator has its own sub-menu. Saved records are grouped
by category, so searching or listing in one menu only shows records
created by that generator.

Available generators
--------------------

Random Password Generator (``RPG``)
    Generates random passwords from letters, with optional digits and
    symbols. Length is configurable.

Memorable Password Generator (``MPG``)
    Generates passphrases by joining randomly selected words.

    .. warning::
        This generator is under construction. Its menu is functional,
        but the interface may change.

PIN Code Generator (``PCG``)
    Generates numeric PIN codes. Length is configurable.

JWT Secret Generator (``JSG``)
    Generates secret keys for signing JSON Web Tokens. The output
    format (``hex``, ``urlsafe``, ``bytes``, or ``custom``) and length
    in bits are configurable.

Main features
-------------

* Generate random passwords, PIN codes, and JWT secrets.
* Configure password, PIN, and secret settings from the menus.
* Save generated values under a user-defined name.
* Search, list, edit, and delete saved records.

Modules
-------

:mod:`pass_classes`
    Password, PIN, and secret generator classes. Each class exposes a
    ``generate()`` method.

:mod:`helpers`
    JSON database access and utility functions. Records are persisted
    through :func:`helpers.save_item`.

:mod:`main_functions`
    Record management operations: :func:`main_functions.search_items`,
    :func:`main_functions.list_items`,
    :func:`main_functions.edit_item`, and
    :func:`main_functions.delete_item`.

Dependencies
------------

The application relies on the modules listed above. The
:mod:`pass_classes` module imports :mod:`nltk`, so the NLTK package
must be installed. The ``words`` corpus must also be downloaded before
the Memorable Password Generator is used with its default vocabulary.

Execution
---------

Run this module directly to start the application:

.. code-block:: console

    $ python main.py

The main menu offers the following options:

1. Random Password Generator (RPG)
2. Memorable Password Generator (MPG)
3. Pin Code Generator (PCG)
4. JWT Secret Generator (JSG)
5. Exit

Each generator menu includes a **Save**, **Search**, **List**,
**Edit**, and **Delete** option for its own category, and an
**Exit** option that returns to the main menu.

Example session:

.. code-block:: text

    ==Password Generator==
    1. Random Password Generator (RPG)
    2. Memorable Password Generator (MPG)
    3. Pin Code Generator (PCG)
    4. JWT Secret Generator (JSG)
    5. Exit
    --------------------------------------------------
    Enter your Choice: 3

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
            "JWT Secret Generator": "JSG",
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
        
            # Create a new memorable password generator instance.
            mpg: pass_classes.MemorablePasswordGenerator = (
                pass_classes.MemorablePasswordGenerator()
            )

            # Generate the initial password.
            password: str = mpg.generate()

            # Available operations for the Mamorable Password Generator.
            memorable_password_generator_choices: list[str] = [
                "Include Capitalization",
                "Change Separator",
                "Number of words",
                "Just give me the MPG",
                "Save this MPG",
                "Search Passwords",
                "List Passwords",
                "Edit a Password",
                "Delete a Password",
                "Exit"
            ]

            # Memorable Password Generator menu loop.
            while True:

                # Display MPG options.
                print("==MPG Options==")

                for i, choice in enumerate(
                    memorable_password_generator_choices,
                    start=1
                ):
                    print(f"{i}. {choice}")

                print("-" * 50)

                # Get the user's MPG menu selection.
                memorable_password_generator_choice: str = input(
                    "Enter your Choice: "
                ).strip()


                # --------------------------------------------
                # Enable Numbers
                # --------------------------------------------

                if memorable_password_generator_choice == "1":

                    # Include Capitalization in future passwords.
                    mpg.capitalization = True

                    # Generate a new password using the updated settings.
                    password = mpg.generate()


                # --------------------------------------------
                # Enable Symbols
                # --------------------------------------------

                elif memorable_password_generator_choice == "2":
                    # Ask the user for desired sparator
                    try:
                        new_separator: str = input("Enter your Separator you want: ")

                        # The Separator must be greater than 1
                        if len(new_separator) != 1:
                            raise ValueError

                    except ValueError:
                        print("Please enter a valid Separator.")
                        continue

                    # Update the Separator 
                    mpg.separator = new_separator
                    
                    # Generate a new password using the updated settings.
                    password = mpg.generate()


                # --------------------------------------------
                # Change Password Length
                # --------------------------------------------

                elif memorable_password_generator_choice == "3":

                    # Ask the user for the desired number of words for password.
                    try:
                        new_number_of_words: int = int(
                            input("Enter your number of words: ")
                        )

                        # Password number of words must be a positive integer.
                        if new_number_of_words < 1:
                            raise ValueError

                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    # Update the generator configuration.
                    mpg.number_of_words = new_number_of_words

                    # Generate a password with the new length.
                    password = mpg.generate()


                # --------------------------------------------
                # Display Current Password
                # --------------------------------------------

                elif memorable_password_generator_choice == "4":

                    print(f"Here is your MPG: {password}")
                    continue


                # --------------------------------------------
                # Save Password
                # --------------------------------------------

                elif memorable_password_generator_choice == "5":

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
                        helpers.save_item(name, password, "mpg")

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

                elif memorable_password_generator_choice == "6":

                    # Search only records belonging to the MPG category.
                    main_functions.search_items("mpg")
                    continue


                # --------------------------------------------
                # List Saved Passwords
                # --------------------------------------------

                elif memorable_password_generator_choice == "7":

                    # Display all saved MPG records.
                    main_functions.list_items("mpg")
                    continue


                # --------------------------------------------
                # Edit a Saved Password
                # --------------------------------------------

                elif memorable_password_generator_choice == "8":

                    # Pass the generator method as a callable.
                    # It allows edit_item() to generate a replacement password.
                    main_functions.edit_item("mpg", mpg.generate)
                    continue


                # --------------------------------------------
                # Delete a Saved Password
                # --------------------------------------------

                elif memorable_password_generator_choice == "9":

                    # Delete a selected RPG record.
                    main_functions.delete_item("mpg")
                    continue


                # --------------------------------------------
                # Exit RPG Menu
                # --------------------------------------------

                elif memorable_password_generator_choice == "10":

                    break


                # --------------------------------------------
                # Invalid Selection
                # --------------------------------------------

                else:
                    print("Please enter correct Choice.")
                    continue


                # Display the current generated password.
                print(f"Here is your MPG: {password}")

                # Ask whether the user wants to leave the RPG menu.
                user_quit_request: str = input(
                    "You want to quit? (yes, no) "
                ).strip().lower()

                if user_quit_request == "yes":
                    break

                elif user_quit_request == "no":
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
        # JWT SECRET GENERATOR MENU
        # ====================================================

        elif user_choice == "4":

            # Create a new JWT secret generator instance.
            jsg: pass_classes.JWTSecretGenerator = (
                pass_classes.JWTSecretGenerator()
            )

            # Generate the initial JWT secret.
            password: str = jsg.generate()

            # Available operations for the JWT Secret Generator.
            jwt_secret_generator_choices: list[str] = [
                "Include Numbers",
                "Include Symbols",
                "Length",
                "Encoding",
                "Just give me the JSG",
                "Save this JSG",
                "Search JWT Secrets",
                "List JWT Secrets",
                "Edit a JWT Secret",
                "Delete a JWT Secret",
                "Exit"
            ]

            # JWT Secret Generator menu loop.
            while True:

                # Display JSG options.
                print("==JSG Options==")

                for i, choice in enumerate(
                    jwt_secret_generator_choices,
                    start=1
                ):
                    print(f"{i}. {choice}")

                print("-" * 50)

                # Get the user's JWT menu selection.
                jwt_secret_generator_choice: str = input(
                    "Enter your Choice: "
                ).strip()


                # --------------------------------------------
                # Enable Numbers
                # --------------------------------------------

                if jwt_secret_generator_choice == "1":

                    # Include numeric characters in future passwords.
                    jsg.include_numbers = True

                    # Generate a new JWT secret using the updated settings.
                    password = jsg.generate()


                # --------------------------------------------
                # Enable Symbols
                # --------------------------------------------

                elif jwt_secret_generator_choice == "2":

                    # Include punctuation characters in future passwords.
                    jsg.include_symbols = True

                    # Generate a new JWT secret using the updated settings.
                    password = jsg.generate()


                # --------------------------------------------
                # Change JWT Secret Length
                # --------------------------------------------

                elif jwt_secret_generator_choice == "3":

                    # Ask the user for the desired Secret length.
                    try:
                        new_length: int = int(
                            input("Enter your Length: ")
                        )

                        # Secret length must be a positive integer.
                        if new_length < 1:
                            raise ValueError

                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    # Update the generator configuration.
                    jsg.length = new_length

                    # Generate a JWT secret with the new length.
                    password = jsg.generate()


                # --------------------------------------------
                # Change JWT Secret Encoding
                # --------------------------------------------

                elif jwt_secret_generator_choice == "4":
                    choices: list[str] = ['hex', 'urlsafe', 'bytes', 'custom']
                    
                    # Ask the user for the desired encoding.
                    new_encoding: str = input(
                        f"Enter your Encoding (e.g., {', '.join(choices)}): "
                    ).strip()

                    # Validate the encoding choice.
                    if new_encoding not in choices:
                        print(f"Invalid encoding. Please choose from: {', '.join(choices)}")
                        continue

                    # Update the generator configuration.
                    jsg.encoding = new_encoding

                    # Generate a JWT secret with the new encoding.
                    password = jsg.generate()


                # --------------------------------------------
                # Display Current JWT Secret
                # --------------------------------------------

                elif jwt_secret_generator_choice == "5":

                    print(f"Here is your JWT Secret: {password}")
                    continue


                # --------------------------------------------
                # Save JWT Secret
                # --------------------------------------------

                elif jwt_secret_generator_choice == "6":

                    # Check whether a JWT secret has been generated.
                    if password:

                        # Get a user-defined name for the JWT secret.
                        name: str = input(
                            "Enter a name for your JWT Secret: "
                        ).strip()

                        if not name:
                            print("Name can't be empty.")
                            continue

                        # Save the password in the JSON database.
                        helpers.save_item(name, password, "jwt")

                        print("JWT Secret saved successfully!")

                    else:
                        print(
                            "There is no JWT Secret. "
                            "Please create one first."
                        )
                        continue


                # --------------------------------------------
                # Search Saved JWT Secrets
                # --------------------------------------------

                elif jwt_secret_generator_choice == "7":

                    # Search only records belonging to the JWT category.
                    main_functions.search_items("jwt")
                    continue


                # --------------------------------------------
                # List Saved JWT Secrets
                # --------------------------------------------

                elif jwt_secret_generator_choice == "8":

                    # Display all saved JWT secrets.
                    main_functions.list_items("jwt")
                    continue


                # --------------------------------------------
                # Edit a Saved JWT Secret
                # --------------------------------------------

                elif jwt_secret_generator_choice == "9":

                    # Pass the generator method as a callable.
                    # It allows edit_item() to generate a replacement password.
                    main_functions.edit_item("jwt", jsg.generate)
                    continue


                # --------------------------------------------
                # Delete a Saved JWT Secret
                # --------------------------------------------

                elif jwt_secret_generator_choice == "10":

                    # Delete a selected JWT secret.
                    main_functions.delete_item("jwt")
                    continue


                # --------------------------------------------
                # Exit JWT Secret Menu
                # --------------------------------------------

                elif jwt_secret_generator_choice == "11":

                    break


                # --------------------------------------------
                # Invalid Selection
                # --------------------------------------------

                else:
                    print("Please enter correct Choice.")
                    continue


                # Display the current generated password.
                print(f"Here is your JWT Secret: {password}")

                # Ask whether the user wants to leave the JWT Secret menu.
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

        elif user_choice == "5":

            # Display the exit message and terminate the main loop.
            print("Bye!")
            break


        # ====================================================
        # INVALID MAIN MENU SELECTION
        # ====================================================

        else:

            # Handle invalid main menu input.
            print("Please enter correct Choice.")
