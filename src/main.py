import pass_classes
import helpers
import main_functions


if __name__ == "__main__":
    while True: 
        choices: dict[str] = {
            "Random Password Generator": "RPG",
            "Memorable Password Generator": "MPG",
            "Pin Code Generator": "PCG",
            "Exit": ""
        }

        print("==Password Generator==")
        for i, (choice, abbr) in enumerate(choices.items()):
            print(f'{i + 1}. {choice} ({abbr})')
        print(50*'-')

        user_choice: str = input('Enter your Choice: ')

        if user_choice == "1": 
            rpg: pass_classes.RandomPasswordGenerator = pass_classes.RandomPasswordGenerator()
            password: str = rpg.generate()
            random_password_generator_choices: list[str] = [
                "Include Numbers", "Include Symbols", "Length", "Just give me the RPG",
                "Save this RPG", "Search Passwords", "List Passwords", "Edit a Password",
                "Delete a Password", "Exit"
            ]
            
            while True: 
                print("==RPG Options==")
                for i, choice in enumerate(random_password_generator_choices):
                    print(f'{i + 1}. {choice}')
                print(50*'-')

                random_password_generator_choice: str = input("Enter your Choice: ")

                if random_password_generator_choice == "1":
                    rpg.include_numbers = True
                    password: str = rpg.generate()
                elif random_password_generator_choice == "2":
                    rpg.include_symbols = True
                    password: str = rpg.generate()
                elif random_password_generator_choice == "3":
                    try:
                        new_length: int = int(input("Enter your Length: "))
                        if new_length < 1:
                            raise ValueError
                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    rpg.length = new_length
                    password: str = rpg.generate()
                elif random_password_generator_choice == "4":
                    print(f'Here is your RPG: {password}')
                    continue
                elif random_password_generator_choice == "5":
                    if password:
                        name: str = input("Enter a name for your Password: ")
                        helpers.save_item(name, password, 'rpg')
                        print("Password saved successfully!")
                    else:
                        print("There is no Password. Please create one first. ")
                        continue
                elif random_password_generator_choice == "6":
                    main_functions.search_items('rpg')
                    continue
                elif random_password_generator_choice == "7":
                    main_functions.list_items('rpg')
                    continue
                elif random_password_generator_choice == "8":
                    main_functions.edit_item('rpg', rpg.generate)
                    continue
                elif random_password_generator_choice == "9":
                    main_functions.delete_item('rpg')
                    continue
                elif random_password_generator_choice == "10":
                    break
                else:
                    print("Please enter correct Choice.")
                    continue

                print(f'Here is your RPG: {password}')

                user_quit_request: str = input("You want to quit? (yes, no) ").strip().lower()

                if user_quit_request == "yes":
                    break
                elif user_quit_request == "no":
                    continue
        elif user_choice == "2":
            print("Under construction. Please try again later. ")
            print(50*'-')
            continue
        elif user_choice == "3":
            pcg: pass_classes.PinCodeGenerator = pass_classes.PinCodeGenerator()
            pin: str = pcg.generate()
            pin_code_generator_choices: list[str] = [
                'Length', 'Just Give me the Pin', 'Save this Pin', 'Search Pins',
                'List Pins', 'Edit a Pin', 'Delete a Pin', 'Exit'
            ]

            while True:
                print("==PCG Options==")
                for i, choice in enumerate(pin_code_generator_choices):
                    print(f'{i + 1}. {choice}')
                print(50*'-')

                pin_code_generator_choice: str = input("Enter your Choice: ")

                if pin_code_generator_choice == "1":
                    try:
                        new_length: int = int(input("Enter your Length: "))
                        if new_length < 1:
                            raise ValueError
                    except ValueError:
                        print("Please enter a correct Number.")
                        continue

                    pcg.length = new_length
                    pin: str = pcg.generate()
                elif pin_code_generator_choice == "2":
                    print(f'Here is your Pin: {pin}')
                    continue
                elif pin_code_generator_choice == "3":
                    if pin: 
                        name: str = input("Enter a name for your Pin: ")
                        helpers.save_item(name, pin, 'pin')
                        print("Pin saved successfully!")
                    else:
                        print("There is no Pin. Please create one first. ")
                        continue
                elif pin_code_generator_choice == "4":
                    main_functions.search_items('pin')
                    continue
                elif pin_code_generator_choice == "5":
                    main_functions.list_items('pin')
                    continue
                elif pin_code_generator_choice == "6":
                    main_functions.edit_item('pin', pcg.generate)
                    continue
                elif pin_code_generator_choice == "7":
                    main_functions.delete_item('pin')
                    continue
                elif pin_code_generator_choice == "8":
                    break
                else:
                    print("Please enter correct Choice.")
                    continue

                print(f'Here is your Pin: {pin}')

                user_quit_request: str = input("You want to quit? (yes, no) ").strip().lower()

                if user_quit_request == "yes":
                    break
                elif user_quit_request == "no":
                    continue
        elif user_choice == "4":
            print("Bye!")
            break   