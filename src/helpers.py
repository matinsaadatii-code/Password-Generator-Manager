import json
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv


# data
load_dotenv()
data_path = os.getenv("DATA_PATH", "data.json")


def load_items() -> list[dict]:
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            items: list[str] = json.load(f)
            if not isinstance(items, list):
                items: list[str] = [items]
    except (FileNotFoundError, json.JSONDecodeError):
        items: list[str] = []
    return items


def save_items(items: list[dict]) -> None:
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)


def now_str() -> str:
    return str(datetime.now().isoformat(sep=" "))


def save_item(name: str, password: str, pass_type: str) -> None:
    items: list[str] = load_items()
    items.append({
        'name': name,
        'password': password,
        'date': now_str(),
        'type': pass_type,
        'id': str(uuid.uuid4()),
    })
    save_items(items)


def get_items_by_type(pass_type: str) -> list[dict]:
    return [item for item in load_items() if item.get("type") == pass_type]


def print_item(item: dict[str]) -> None:
    print(50 * '-')
    print(f'name: {item["name"]}')
    print(f'password: {item["password"]}')
    print(f'date: {item["date"]}')
    if item.get("updated"):
        print(f'updated: {item["updated"]}')
    print(f'id: {item["id"]}')
    print(50 * '-')