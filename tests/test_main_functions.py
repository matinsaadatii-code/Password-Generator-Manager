import uuid

import pytest

from src import main_functions
from src import helpers

def make_item(name="gmail", password="pw", pass_type="rpg", **extra):
    item = {
        "name": name,
        "password": password,
        "date": "2026-01-01 10:00:00",
        "type": pass_type,
        "id": str(uuid.uuid4()),
    }
    item.update(extra)
    return item


@pytest.fixture
def items(data_file):
    """Three saved records: two rpg and one pin."""
    data = [
        make_item("Gmail", "Abc123", "rpg"),
        make_item("Github", "xyz789", "rpg"),
        make_item("Bank", "1234", "pin"),
    ]
    helpers.save_items(data)
    return data


# ====================================================
# search_items
# ====================================================

class TestSearchItems:
    def test_by_name_partial_case_insensitive(self, items, fake_input, capsys):
        fake_input("1", "  GM ")
        main_functions.search_items("rpg")
        out = capsys.readouterr().out
        assert "Found 1 item(s)!" in out
        assert "Name: Gmail" in out
        assert "Github" not in out

    def test_by_name_multiple_results(self, items, fake_input, capsys):
        fake_input("1", "g")
        main_functions.search_items("rpg")
        out = capsys.readouterr().out
        assert "Found 2 item(s)!" in out
        assert "Name: Gmail" in out and "Name: Github" in out

    def test_by_id_exact(self, items, fake_input, capsys):
        fake_input("2", items[1]["id"])
        main_functions.search_items("rpg")
        out = capsys.readouterr().out
        assert "Found 1 item(s)!" in out
        assert "Name: Github" in out

    def test_by_id_partial_not_found(self, items, fake_input, capsys):
        fake_input("2", items[0]["id"][:8])
        main_functions.search_items("rpg")
        assert "Not found." in capsys.readouterr().out

    def test_by_password_exact(self, items, fake_input, capsys):
        fake_input("3", "xyz789")
        main_functions.search_items("rpg")
        out = capsys.readouterr().out
        assert "Found 1 item(s)!" in out
        assert "Name: Github" in out

    def test_by_password_partial_not_found(self, items, fake_input, capsys):
        fake_input("3", "xyz")
        main_functions.search_items("rpg")
        assert "Not found." in capsys.readouterr().out

    def test_by_password_is_case_sensitive(self, items, fake_input, capsys):
        fake_input("3", "abc123")
        main_functions.search_items("rpg")
        assert "Not found." in capsys.readouterr().out

    def test_only_searches_given_type(self, items, fake_input, capsys):
        fake_input("1", "bank")
        main_functions.search_items("rpg")
        assert "Not found." in capsys.readouterr().out

    def test_pin_type_finds_pin(self, items, fake_input, capsys):
        fake_input("3", "1234")
        main_functions.search_items("pin")
        assert "Name: Bank" in capsys.readouterr().out

    def test_back_returns_silently(self, items, fake_input, capsys):
        fake_input("4")
        assert main_functions.search_items("rpg") is None
        out = capsys.readouterr().out
        assert "Not found" not in out and "Found" not in out

    @pytest.mark.parametrize("bad", ["", "9", "abc", "0"])
    def test_invalid_choice(self, items, fake_input, capsys, bad):
        fake_input(bad)
        main_functions.search_items("rpg")
        assert "Please enter correct Choice." in capsys.readouterr().out

    def test_menu_is_printed(self, items, fake_input, capsys):
        fake_input("4")
        main_functions.search_items("rpg")
        out = capsys.readouterr().out
        assert "==Search Options==" in out
        assert "1. Search by Name" in out
        assert "4. Back" in out

    def test_no_saved_items(self, data_file, fake_input, capsys):
        fake_input("1", "x")
        main_functions.search_items("rpg")
        assert "Not found." in capsys.readouterr().out


# ====================================================
# list_items
# ====================================================

class TestListItems:
    def test_empty(self, data_file, capsys):
        assert main_functions.list_items("rpg") == []
        assert "There are no saved items yet." in capsys.readouterr().out

    def test_returns_items_of_type(self, items):
        result = main_functions.list_items("rpg")
        assert result == items[:2]

    def test_prints_numbered_rows(self, items, capsys):
        main_functions.list_items("rpg")
        out = capsys.readouterr().out
        assert "==Saved items (2)==" in out
        assert "1. Gmail | Abc123 | 2026-01-01 10:00:00" in out
        assert "2. Github | xyz789 | 2026-01-01 10:00:00" in out

    def test_does_not_list_other_type(self, items, capsys):
        main_functions.list_items("rpg")
        assert "Bank" not in capsys.readouterr().out

    def test_pin_list(self, items, capsys):
        result = main_functions.list_items("pin")
        assert result == [items[2]]
        assert "==Saved items (1)==" in capsys.readouterr().out

    def test_type_with_no_records(self, items, capsys):
        assert main_functions.list_items("other") == []
        assert "There are no saved items yet." in capsys.readouterr().out


# ====================================================
# pick_item
# ====================================================

class TestPickItem:
    def test_no_items_returns_none_without_asking(self, data_file, fake_input):
        fake_input()  # any input() call would fail the test
        assert main_functions.pick_item("rpg", "edit") is None

    def test_valid_choice_is_one_based(self, items, fake_input):
        fake_input("1")
        assert main_functions.pick_item("rpg", "edit") == items[0]

    def test_second_item(self, items, fake_input):
        fake_input(" 2 ")
        assert main_functions.pick_item("rpg", "edit") == items[1]

    def test_enter_cancels(self, items, fake_input, capsys):
        fake_input("")
        assert main_functions.pick_item("rpg", "edit") is None
        assert "Please enter" not in capsys.readouterr().out

    @pytest.mark.parametrize("bad", ["abc", "0", "3", "-1", "1.5", "99"])
    def test_invalid_choice(self, items, fake_input, capsys, bad):
        fake_input(bad)
        assert main_functions.pick_item("rpg", "edit") is None
        assert "Please enter a correct Number." in capsys.readouterr().out

    def test_prompt_contains_action(self, items, monkeypatch):
        prompts = []

        def _input(prompt=""):
            prompts.append(prompt)
            return ""

        monkeypatch.setattr("builtins.input", _input)
        main_functions.pick_item("rpg", "delete")
        assert "delete" in prompts[0]

    def test_uses_only_given_type(self, items, fake_input, capsys):
        fake_input("2")
        # only one pin exists, so 2 is out of range
        assert main_functions.pick_item("pin", "edit") is None
        assert "Please enter a correct Number." in capsys.readouterr().out


# ====================================================
# update_item
# ====================================================

class TestUpdateItem:
    def test_update_existing(self, items, monkeypatch):
        monkeypatch.setattr(helpers, "now_str", lambda: "2026-05-05 05:05:05")
        assert main_functions.update_item(items[0]["id"], name="New") is True
        saved = helpers.load_items()[0]
        assert saved["name"] == "New"
        assert saved["updated"] == "2026-05-05 05:05:05"
        assert saved["password"] == "Abc123"

    def test_update_multiple_fields(self, items):
        main_functions.update_item(items[1]["id"], name="N", password="P")
        saved = helpers.load_items()[1]
        assert (saved["name"], saved["password"]) == ("N", "P")

    def test_unknown_id_returns_false_and_file_unchanged(self, items):
        assert main_functions.update_item("no-such-id", name="X") is False
        assert helpers.load_items() == items

    def test_other_records_untouched(self, items):
        main_functions.update_item(items[0]["id"], name="New")
        saved = helpers.load_items()
        assert saved[1:] == items[1:]

    def test_no_file(self, data_file):
        assert main_functions.update_item("x", name="y") is False

    def test_update_without_changes_still_sets_updated(self, items):
        assert main_functions.update_item(items[0]["id"]) is True
        assert "updated" in helpers.load_items()[0]


# ====================================================
# edit_item
# ====================================================

class TestEditItem:
    def test_no_items(self, data_file, fake_input):
        fake_input()
        assert main_functions.edit_item("rpg", lambda: "x") is None

    def test_cancel_at_pick(self, items, fake_input):
        fake_input("")
        main_functions.edit_item("rpg", lambda: "x")
        assert helpers.load_items() == items

    def test_change_name(self, items, fake_input, capsys):
        fake_input("1", "1", " Renamed ")
        main_functions.edit_item("rpg", lambda: "x")
        saved = helpers.load_items()[0]
        assert saved["name"] == "Renamed"
        assert "updated" in saved
        out = capsys.readouterr().out
        assert "You are editing:" in out
        assert "Item updated successfully!" in out

    def test_empty_name_rejected(self, items, fake_input, capsys):
        fake_input("1", "1", "   ")
        main_functions.edit_item("rpg", lambda: "x")
        assert "Name can't be empty." in capsys.readouterr().out
        assert helpers.load_items() == items

    def test_change_password_manually(self, items, fake_input, capsys):
        fake_input("2", "2", "NewPass!")
        main_functions.edit_item("rpg", lambda: "x")
        assert helpers.load_items()[1]["password"] == "NewPass!"
        assert "Item updated successfully!" in capsys.readouterr().out

    def test_empty_password_rejected(self, items, fake_input, capsys):
        fake_input("1", "2", "")
        main_functions.edit_item("rpg", lambda: "x")
        assert "Value can't be empty." in capsys.readouterr().out
        assert helpers.load_items() == items

    def test_generate_new_password(self, items, fake_input, capsys):
        calls = []

        def gen():
            calls.append(1)
            return "GENERATED"

        fake_input("1", "3")
        main_functions.edit_item("rpg", gen)
        assert len(calls) == 1
        assert helpers.load_items()[0]["password"] == "GENERATED"
        out = capsys.readouterr().out
        assert "New value: GENERATED" in out
        assert "Item updated successfully!" in out

    def test_generate_not_called_for_other_choices(self, items, fake_input):
        def gen():
            raise AssertionError("generate must not be called")

        fake_input("1", "1", "Name")
        main_functions.edit_item("rpg", gen)

    @pytest.mark.parametrize("choice", ["4", "9", "", "abc"])
    def test_cancel_or_invalid_choice(self, items, fake_input, capsys, choice):
        fake_input("1", choice)
        main_functions.edit_item("rpg", lambda: "x")
        assert "Edit cancelled." in capsys.readouterr().out
        assert helpers.load_items() == items

    def test_edit_pin_type(self, items, fake_input):
        fake_input("1", "3")
        main_functions.edit_item("pin", lambda: "9999")
        assert helpers.load_items()[2]["password"] == "9999"

    def test_edit_shows_selected_item(self, items, fake_input, capsys):
        fake_input("2", "4")
        main_functions.edit_item("rpg", lambda: "x")
        assert "Name: Github" in capsys.readouterr().out


# ====================================================
# delete_item
# ====================================================

class TestDeleteItem:
    def test_no_items(self, data_file, fake_input):
        fake_input()
        assert main_functions.delete_item("rpg") is None

    def test_cancel_at_pick(self, items, fake_input):
        fake_input("")
        main_functions.delete_item("rpg")
        assert helpers.load_items() == items

    def test_confirm_yes_deletes(self, items, fake_input, capsys):
        fake_input("1", "yes")
        main_functions.delete_item("rpg")
        assert helpers.load_items() == items[1:]
        assert "Item deleted successfully!" in capsys.readouterr().out

    @pytest.mark.parametrize("answer", ["YES", " Yes "])
    def test_confirm_is_case_and_space_insensitive(self, items, fake_input, answer):
        fake_input("2", answer)
        main_functions.delete_item("rpg")
        assert [i["name"] for i in helpers.load_items()] == ["Gmail", "Bank"]

    @pytest.mark.parametrize("answer", ["no", "", "y", "yes please", "abc"])
    def test_anything_else_cancels(self, items, fake_input, capsys, answer):
        fake_input("1", answer)
        main_functions.delete_item("rpg")
        assert "Delete cancelled." in capsys.readouterr().out
        assert helpers.load_items() == items

    def test_other_types_untouched(self, items, fake_input):
        fake_input("1", "yes")
        main_functions.delete_item("pin")
        saved = helpers.load_items()
        assert items[2] not in saved
        assert items[0] in saved and items[1] in saved

    def test_invalid_pick_deletes_nothing(self, items, fake_input, capsys):
        fake_input("99")
        main_functions.delete_item("rpg")
        assert "Please enter a correct Number." in capsys.readouterr().out
        assert helpers.load_items() == items

    def test_shows_item_before_confirm(self, items, fake_input, capsys):
        fake_input("1", "no")
        main_functions.delete_item("rpg")
        assert "Name: Gmail" in capsys.readouterr().out