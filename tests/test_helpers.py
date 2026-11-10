import json
import re
import uuid
from datetime import datetime as real_datetime

import pytest

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


# ====================================================
# load_items
# ====================================================

class TestLoadItems:
    def test_missing_file_returns_empty_list(self, data_file):
        assert helpers.load_items() == []

    def test_invalid_json_returns_empty_list(self, data_file):
        data_file.write_text("{not valid json", encoding="utf-8")
        assert helpers.load_items() == []

    def test_empty_file_returns_empty_list(self, data_file):
        data_file.write_text("", encoding="utf-8")
        assert helpers.load_items() == []

    def test_empty_list(self, data_file):
        data_file.write_text("[]", encoding="utf-8")
        assert helpers.load_items() == []

    def test_list_is_returned_as_is(self, data_file):
        items = [make_item("a"), make_item("b")]
        data_file.write_text(json.dumps(items), encoding="utf-8")
        assert helpers.load_items() == items

    def test_single_dict_is_wrapped_in_list(self, data_file):
        item = make_item()
        data_file.write_text(json.dumps(item), encoding="utf-8")
        assert helpers.load_items() == [item]

    @pytest.mark.parametrize("content", ["123", '"text"', "null", "true"])
    def test_unexpected_root_type_returns_empty_list(self, data_file, content):
        data_file.write_text(content, encoding="utf-8")
        assert helpers.load_items() == []

    def test_reads_persian_utf8(self, data_file):
        items = [make_item(name="ایمیل")]
        data_file.write_text(
            json.dumps(items, ensure_ascii=False), encoding="utf-8"
        )
        assert helpers.load_items()[0]["name"] == "ایمیل"


# ====================================================
# save_items
# ====================================================

class TestSaveItems:
    def test_round_trip(self, data_file):
        items = [make_item("a"), make_item("b", pass_type="pin")]
        helpers.save_items(items)
        assert helpers.load_items() == items

    def test_overwrites_previous_content(self, data_file):
        helpers.save_items([make_item("old")])
        new = [make_item("new")]
        helpers.save_items(new)
        assert helpers.load_items() == new

    def test_empty_list(self, data_file):
        helpers.save_items([])
        assert json.loads(data_file.read_text(encoding="utf-8")) == []

    def test_persian_is_not_escaped(self, data_file):
        helpers.save_items([make_item(name="ایمیل")])
        text = data_file.read_text(encoding="utf-8")
        assert "ایمیل" in text
        assert "\\u" not in text

    def test_file_is_indented(self, data_file):
        helpers.save_items([make_item()])
        assert "\n    " in data_file.read_text(encoding="utf-8")

    def test_missing_parent_directory_raises(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            helpers, "DATA_PATH", str(tmp_path / "missing" / "data.json")
        )
        with pytest.raises(FileNotFoundError):
            helpers.save_items([])


# ====================================================
# now_str
# ====================================================

class TestNowStr:
    def test_format(self):
        value = helpers.now_str()
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value)

    def test_is_parseable(self):
        real_datetime.strptime(helpers.now_str(), "%Y-%m-%d %H:%M:%S")

    def test_uses_current_datetime(self, monkeypatch):
        class FakeDatetime:
            @staticmethod
            def now():
                return real_datetime(2026, 11, 10, 14, 30, 5, 999)

        monkeypatch.setattr(helpers, "datetime", FakeDatetime)
        assert helpers.now_str() == "2026-11-10 14:30:05"


# ====================================================
# save_item
# ====================================================

class TestSaveItem:
    def test_creates_file_and_record(self, data_file):
        helpers.save_item("gmail", "secret", "rpg")
        items = helpers.load_items()
        assert len(items) == 1
        assert items[0]["name"] == "gmail"
        assert items[0]["password"] == "secret"
        assert items[0]["type"] == "rpg"

    def test_record_has_expected_keys(self, data_file):
        helpers.save_item("a", "b", "pin")
        assert set(helpers.load_items()[0]) == {
            "name", "password", "date", "type", "id"
        }

    def test_id_is_valid_uuid4(self, data_file):
        helpers.save_item("a", "b", "rpg")
        parsed = uuid.UUID(helpers.load_items()[0]["id"])
        assert parsed.version == 4

    def test_date_comes_from_now_str(self, data_file, monkeypatch):
        monkeypatch.setattr(helpers, "now_str", lambda: "2026-01-02 03:04:05")
        helpers.save_item("a", "b", "rpg")
        assert helpers.load_items()[0]["date"] == "2026-01-02 03:04:05"

    def test_appends_to_existing_records(self, data_file):
        first = make_item("first")
        helpers.save_items([first])
        helpers.save_item("second", "pw", "pin")
        items = helpers.load_items()
        assert len(items) == 2
        assert items[0] == first
        assert items[1]["name"] == "second"

    def test_ids_are_unique(self, data_file):
        helpers.save_item("a", "1", "rpg")
        helpers.save_item("b", "2", "rpg")
        ids = [i["id"] for i in helpers.load_items()]
        assert len(set(ids)) == 2

    def test_persian_name(self, data_file):
        helpers.save_item("بانک", "1234", "pin")
        assert helpers.load_items()[0]["name"] == "بانک"


# ====================================================
# get_items_by_type
# ====================================================

class TestGetItemsByType:
    def test_filters_by_type(self, data_file):
        rpg = make_item("a", pass_type="rpg")
        pin = make_item("b", pass_type="pin")
        helpers.save_items([rpg, pin])
        assert helpers.get_items_by_type("rpg") == [rpg]
        assert helpers.get_items_by_type("pin") == [pin]

    def test_returns_all_matching(self, data_file):
        items = [make_item("a"), make_item("b"), make_item("c", pass_type="pin")]
        helpers.save_items(items)
        assert len(helpers.get_items_by_type("rpg")) == 2

    def test_no_match_returns_empty_list(self, data_file):
        helpers.save_items([make_item(pass_type="rpg")])
        assert helpers.get_items_by_type("pin") == []

    def test_no_file_returns_empty_list(self, data_file):
        assert helpers.get_items_by_type("rpg") == []

    def test_item_without_type_is_ignored(self, data_file):
        no_type = make_item()
        del no_type["type"]
        helpers.save_items([no_type, make_item("b", pass_type="rpg")])
        result = helpers.get_items_by_type("rpg")
        assert [i["name"] for i in result] == ["b"]


# ====================================================
# print_item
# ====================================================

class TestPrintItem:
    def test_prints_all_fields(self, capsys):
        item = make_item("gmail", "secret")
        helpers.print_item(item)
        out = capsys.readouterr().out
        assert "Name: gmail" in out
        assert "Password/PIN: secret" in out
        assert "Date: 2026-01-01 10:00:00" in out
        assert f"ID: {item['id']}" in out

    def test_updated_shown_when_present(self, capsys):
        helpers.print_item(make_item(updated="2026-02-02 11:11:11"))
        assert "Updated: 2026-02-02 11:11:11" in capsys.readouterr().out

    def test_updated_hidden_when_absent(self, capsys):
        helpers.print_item(make_item())
        assert "Updated:" not in capsys.readouterr().out

    def test_updated_hidden_when_empty(self, capsys):
        helpers.print_item(make_item(updated=""))
        assert "Updated:" not in capsys.readouterr().out

    def test_separator_lines(self, capsys):
        helpers.print_item(make_item())
        lines = capsys.readouterr().out.splitlines()
        assert lines[0] == "-" * 50
        assert lines[-1] == "-" * 50

    @pytest.mark.parametrize("missing", ["name", "password", "date", "id"])
    def test_missing_required_key_raises_keyerror(self, missing):
        item = make_item()
        del item[missing]
        with pytest.raises(KeyError):
            helpers.print_item(item)