import helpers
from typing import Callable, Optional


def search_items(pass_type: str) -> None:
    options = ['Search by Name', 'Search by Id', 'Search by Password/Pin', 'Back']

    print("==Search Options==")
    for i, option in enumerate(options):
        print(f'{i + 1}. {option}')
    print(50 * '-')

    choice = input("Enter your Choice: ").strip()
    items = helpers.get_items_by_type(pass_type)

    if choice == '1':
        query = input("Enter the name: ").strip().lower()
        results = [item for item in items if query in item["name"].lower()]
    elif choice == '2':
        query = input("Enter the id: ").strip()
        results = [item for item in items if item["id"] == query]
    elif choice == '3':
        query = input("Enter the Password/Pin: ")
        results = [item for item in items if item["password"] == query]
    elif choice == '4':
        return
    else:
        print("Please enter correct Choice.")
        return

    if not results:
        print("Not found.")
        return

    print(f"Found {len(results)} item(s)!")
    for item in results:
        helpers.print_item(item)


def list_items(pass_type: str) -> list[dict]:
    items = helpers.get_items_by_type(pass_type)

    if not items:
        print("There are no saved items yet.")
        return items

    print(f"==Saved items ({len(items)})==")
    for i, item in enumerate(items, start=1):
        print(f'{i}. {item["name"]} | {item["password"]} | {item["date"]}')
    print(50 * '-')
    return items


def pick_item(pass_type: str, action: str) -> Optional[dict]:
    items = list_items(pass_type)
    if not items:
        return None

    choice = input(f"Enter the number of the item you want to {action} (Enter to cancel): ").strip()
    if not choice:
        return None

    if not choice.isdigit() or not 1 <= int(choice) <= len(items):
        print("Please enter a correct Number.")
        return None

    return items[int(choice) - 1]


def update_item(item_id: str, **changes) -> bool:
    items = helpers.load_items()
    for item in items:
        if item.get("id") == item_id:
            item.update(changes)
            item["updated"] = helpers.now_str()
            helpers.save_items(items)
            return True
    return False


def edit_item(pass_type: str, generate: Callable[[], str]) -> None:
    item = pick_item(pass_type, "edit")
    if item is None:
        return

    print("You are editing:")
    helpers.print_item(item)

    options = ['Change name', 'Change password/pin manually', 'Generate a new one', 'Cancel']
    print("==Edit Options==")
    for i, option in enumerate(options):
        print(f'{i + 1}. {option}')
    print(50 * '-')

    choice = input("Enter your Choice: ").strip()

    if choice == '1':
        new_name = input("Enter the new name: ").strip()
        if not new_name:
            print("Name can't be empty.")
            return
        update_item(item["id"], name=new_name)
    elif choice == '2':
        new_password = input("Enter the new password/pin: ")
        if not new_password:
            print("Value can't be empty.")
            return
        update_item(item["id"], password=new_password)
    elif choice == '3':
        new_password = generate()
        update_item(item["id"], password=new_password)
        print(f'New value: {new_password}')
    else:
        print("Edit cancelled.")
        return

    print("Item updated successfully!")


def delete_item(pass_type: str) -> None:
    item = pick_item(pass_type, "delete")
    if item is None:
        return

    helpers.print_item(item)
    confirm = input("Are you sure you want to delete this item? (yes, no) ").strip().lower()

    if confirm != "yes":
        print("Delete cancelled.")
        return

    items = [i for i in helpers.load_items() if i.get("id") != item["id"]]
    helpers.save_items(items)
    print("Item deleted successfully!")

