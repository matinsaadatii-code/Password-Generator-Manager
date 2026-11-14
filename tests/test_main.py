import os
import re
import runpy

import pytest

from src import helpers
from src.pass_classes import secrets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
MAIN = os.path.join(SRC, "main.py")


import importlib
import sys

@pytest.fixture(autouse=True)
def app_env(monkeypatch, data_file):
    monkeypatch.syspath_prepend(SRC)
    monkeypatch.setattr(secrets, "choice", lambda seq: seq[0])

    # ماژولی که main.py با `import helpers` می‌گیرد
    top_helpers = importlib.import_module("helpers")
    monkeypatch.setattr(top_helpers, "DATA_PATH", helpers.DATA_PATH)
    # تست‌ها هم باید از همین ماژول بخوانند
    monkeypatch.setattr(sys.modules[__name__], "helpers", top_helpers)
    


def run_app(fake_input, *answers):
    """Run main.py as a script with the given answers to input()."""
    fake_input(*answers)
    runpy.run_path(MAIN, run_name="__main__")


def last_match(pattern, out):
    matches = re.findall(pattern, out)
    assert matches, f"pattern {pattern!r} not found in output"
    return matches[-1]


# ====================================================
# Main menu
# ====================================================

# class TestMainMenu:
#     def test_exit_prints_bye(self, fake_input, capsys):
#         run_app(fake_input, "4")
#         out = capsys.readouterr().out
#         assert "==Password Generator==" in out
#         assert "Bye!" in out

#     def test_menu_lists_all_options(self, fake_input, capsys):
#         run_app(fake_input, "4")
#         out = capsys.readouterr().out
#         assert "1. Random Password Generator (RPG)" in out
#         assert "2. Memorable Password Generator (MPG)" in out
#         assert "3. Pin Code Generator (PCG)" in out
#         assert "4. Exit ()" in out

#     @pytest.mark.parametrize("bad", ["", "0", "5", "abc"])
#     def test_invalid_main_choice_then_exit(self, fake_input, capsys, bad):
#         run_app(fake_input, bad, "4")
#         out = capsys.readouterr().out
#         assert "Please enter correct Choice." in out
#         assert "Bye!" in out

#     def test_input_is_stripped(self, fake_input, capsys):
#         run_app(fake_input, "  4  ")
#         assert "Bye!" in capsys.readouterr().out

#     def test_memorable_under_construction(self, fake_input, capsys):
#         run_app(fake_input, "2", "4")
#         out = capsys.readouterr().out
#         assert "Under construction. Please try again later." in out
#         assert "Bye!" in out


# # ====================================================
# # RPG menu
# # ====================================================

# class TestRpgMenu:
#     def test_back_from_rpg_to_main(self, fake_input, capsys):
#         run_app(fake_input, "1", "10", "4")
#         out = capsys.readouterr().out
#         assert "==RPG Options==" in out
#         assert "Bye!" in out

#     def test_show_current_password_without_quit_prompt(self, fake_input, capsys):
#         run_app(fake_input, "1", "4", "10", "4")
#         out = capsys.readouterr().out
#         assert "Here is your RPG: " in out
#         assert "You want to quit?" not in out.split("Here is your RPG: ")[1].split("==RPG Options==")[0]

#     def test_generated_password_is_shown_after_action(self, fake_input, capsys):
#         run_app(fake_input, "1", "1", "no", "10", "4")
#         out = capsys.readouterr().out
#         # quit prompt is an input() prompt, so it is not in captured stdout;
#         # the password is shown once after the action, then the menu repeats.
#         assert "Here is your RPG: " in out
#         assert out.count("==RPG Options==") == 2

#     def test_quit_yes_returns_to_main(self, fake_input, capsys):
#         run_app(fake_input, "1", "2", "yes", "4")
#         out = capsys.readouterr().out
#         assert out.count("==RPG Options==") == 1
#         assert "Bye!" in out

#     def test_quit_no_stays_in_rpg(self, fake_input, capsys):
#         run_app(fake_input, "1", "2", "no", "10", "4")
#         assert capsys.readouterr().out.count("==RPG Options==") == 2

#     def test_length_changes_password(self, fake_input, capsys):
#         run_app(fake_input, "1", "3", "12", "yes", "4")
#         pw = last_match(r"Here is your RPG: (\S+)", capsys.readouterr().out)
#         assert len(pw) == 12

#     @pytest.mark.parametrize("bad", ["abc", "0", "-3", ""])
#     def test_length_invalid_number(self, fake_input, capsys, bad):
#         run_app(fake_input, "1", "3", bad, "10", "4")
#         out = capsys.readouterr().out
#         assert "Please enter a correct Number." in out

#     def test_length_invalid_does_not_ask_quit(self, fake_input, capsys):
#         run_app(fake_input, "1", "3", "x", "10", "4")
#         assert "You want to quit?" not in capsys.readouterr().out

#     def test_invalid_rpg_choice(self, fake_input, capsys):
#         run_app(fake_input, "1", "99", "10", "4")
#         assert "Please enter correct Choice." in capsys.readouterr().out

#     def test_save_empty_name(self, fake_input, capsys, data_file):
#         run_app(fake_input, "1", "5", "", "10", "4")
#         out = capsys.readouterr().out
#         assert "Name can't be empty." in out
#         assert helpers.load_items() == []

#     def test_save_password(self, fake_input, capsys):
#         run_app(fake_input, "1", "5", "Mail", "yes", "4")
#         out = capsys.readouterr().out
#         assert "Password saved successfully!" in out
#         items = helpers.load_items()
#         assert len(items) == 1
#         assert items[0]["name"] == "Mail"
#         assert items[0]["type"] == "rpg"
#         assert items[0]["password"]

#     def test_saved_password_matches_displayed(self, fake_input, capsys):
#         run_app(fake_input, "1", "5", "Mail", "yes", "4")
#         shown = last_match(r"Here is your RPG: (\S+)", capsys.readouterr().out)
#         assert helpers.load_items()[0]["password"] == shown

#     def test_search_uses_rpg_menu(self, fake_input, capsys):
#         run_app(fake_input, "1", "6", "4", "10", "4")
#         out = capsys.readouterr().out
#         assert "==Search Options==" in out

#     def test_list_empty(self, fake_input, capsys):
#         run_app(fake_input, "1", "7", "10", "4")
#         assert "There are no saved items yet." in capsys.readouterr().out

#     def test_edit_empty(self, fake_input, capsys):
#         run_app(fake_input, "1", "8", "10", "4")
#         out = capsys.readouterr().out
#         assert "There are no saved items yet." in out

#     def test_delete_empty(self, fake_input, capsys):
#         run_app(fake_input, "1", "9", "10", "4")
#         assert "There are no saved items yet." in capsys.readouterr().out

#     def test_list_shows_saved_rpg(self, fake_input, capsys):
#         run_app(fake_input, "1", "5", "Mail", "yes", "1", "7", "10", "4")
#         assert "Mail" in capsys.readouterr().out


# # ====================================================
# # PIN menu
# # ====================================================

# class TestPinMenu:
#     def test_back_from_pin_to_main(self, fake_input, capsys):
#         run_app(fake_input, "3", "8", "4")
#         out = capsys.readouterr().out
#         assert "==PCG Options==" in out
#         assert "Bye!" in out

#     def test_show_current_pin(self, fake_input, capsys):
#         run_app(fake_input, "3", "2", "8", "4")
#         assert "Here is your Pin: " in capsys.readouterr().out

#     def test_quit_yes_returns_to_main(self, fake_input, capsys):
#         run_app(fake_input, "3", "1", "6", "yes", "4")
#         out = capsys.readouterr().out
#         assert out.count("==PCG Options==") == 1
#         assert "Here is your Pin: " in out

#     def test_quit_no_stays_in_pin(self, fake_input, capsys):
#         run_app(fake_input, "3", "1", "no", "8", "4")
#         assert capsys.readouterr().out.count("==PCG Options==") == 2

#     def test_length_changes_pin(self, fake_input, capsys):
#         run_app(fake_input, "3", "1", "6", "yes", "4")
#         pin = last_match(r"Here is your Pin: (\S+)", capsys.readouterr().out)
#         assert len(pin) == 6
#         assert pin.isdigit()

#     @pytest.mark.parametrize("bad", ["abc", "0", "-1"])
#     def test_length_invalid(self, fake_input, capsys, bad):
#         run_app(fake_input, "3", "1", bad, "8", "4")
#         assert "Please enter a correct Number." in capsys.readouterr().out

#     def test_invalid_pin_choice(self, fake_input, capsys):
#         run_app(fake_input, "3", "42", "8", "4")
#         assert "Please enter correct Choice." in capsys.readouterr().out

#     def test_save_empty_name(self, fake_input, capsys):
#         run_app(fake_input, "3", "3", "", "8", "4")
#         out = capsys.readouterr().out
#         assert "Name can't be empty." in out
#         assert helpers.load_items() == []

#     def test_save_pin(self, fake_input, capsys):
#         run_app(fake_input, "3", "3", "Card", "yes", "4")
#         out = capsys.readouterr().out
#         assert "Pin saved successfully!" in out
#         items = helpers.load_items()
#         assert len(items) == 1
#         assert items[0]["name"] == "Card"
#         assert items[0]["type"] == "pin"

#     def test_saved_pin_matches_displayed(self, fake_input, capsys):
#         run_app(fake_input, "3", "3", "Card", "yes", "4")
#         shown = last_match(r"Here is your Pin: (\S+)", capsys.readouterr().out)
#         assert helpers.load_items()[0]["password"] == shown

#     def test_search_pins(self, fake_input, capsys):
#         run_app(fake_input, "3", "4", "4", "8", "4")
#         assert "==Search Options==" in capsys.readouterr().out

#     def test_list_pins_shows_only_pins(self, fake_input, capsys):
#         run_app(
#             fake_input,
#             "1", "5", "Mail", "yes",  # RPG saved
#             "3", "3", "Card", "yes",  # PIN saved
#             "3", "5", "8",            # list pins
#             "4",
#         )
#         out = capsys.readouterr().out
#         listing = out.split("==Saved items (1)==")[-1]
#         assert "Card" in listing
#         assert "Mail" not in listing

#     def test_edit_and_delete_empty(self, fake_input, capsys):
#         run_app(fake_input, "3", "6", "7", "8", "4")
#         out = capsys.readouterr().out
#         assert out.count("There are no saved items yet.") == 2