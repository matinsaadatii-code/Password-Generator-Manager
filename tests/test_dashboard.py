import json
from pathlib import Path
from streamlit.testing.v1 import AppTest
# from src import helpers

APP = str(Path(__file__).resolve().parent.parent / "src" / "dashboard.py")


def new_app():
    return AppTest.from_file(APP, default_timeout=10).run()


def button(at, label):
    return next(b for b in at.button if b.label == label)


def saved_items(tmp_data):
    if not tmp_data.exists():
        return []
    return json.loads(tmp_data.read_text(encoding="utf-8"))


# ---------- Generate ----------

def test_app_starts_without_exception():
    at = new_app()
    assert not at.exception


def test_generate_shows_password():
    at = new_app()
    button(at, "Generate").click().run()
    assert not at.exception
    assert len(at.code) == 1
    assert at.code[0].value  # رمز نمایش داده شده نباید خالی باشد


def test_generate_does_not_save_by_itself(tmp_data):
    at = new_app()
    button(at, "Generate").click().run()
    assert saved_items(tmp_data) == []


# def test_typing_name_does_not_save(tmp_data):
#     at = new_app()
#     button(at, "Generate").click().run()
#     at.text_input(key="name_rpg").input("t").run()
#     at.text_input(key="name_rpg").input("te").run()
#     assert saved_items(tmp_data) == []


# # ---------- Save ----------

# def test_save_stores_same_password_that_was_shown(tmp_data):
#     at = new_app()
#     button(at, "Generate").click().run()
#     shown = at.code[0].value

#     at.text_input(key="name_rpg").input("github").run()
#     button(at, "Save").click().run()

#     items = saved_items(tmp_data)
#     assert len(items) == 1
#     assert items[0]["name"] == "github"
#     assert items[0]["password"] == shown
#     assert items[0]["type"] == "rpg" if "type" in items[0] else True


# def test_save_with_empty_name_shows_warning(tmp_data):
#     at = new_app()
#     button(at, "Generate").click().run()
#     button(at, "Save").click().run()
#     assert len(at.warning) == 1
#     assert saved_items(tmp_data) == []


# def test_each_type_saves_with_its_own_type(tmp_data):
#     at = new_app()
#     at.sidebar.radio[0].set_value("Pin Code").run()
#     button(at, "Generate").click().run()
#     at.text_input(key="name_pin").input("card").run()
#     button(at, "Save").click().run()
#     assert saved_items(tmp_data)[0].get("type") == "pin"


# # ---------- JWT ----------

# def test_jwt_invalid_encoding_is_not_possible():
#     # selectbox فقط مقادیر معتبر را دارد، پس باید گزینه‌ها دقیقاً همین‌ها باشند
#     at = new_app()
#     at.sidebar.radio[0].set_value("JWT Secret").run()
#     box = at.selectbox[0]
#     assert list(box.options) == ["hex", "urlsafe", "bytes", "custom"]


# def test_jwt_bytes_encoding_is_saved_as_hex(tmp_data):
#     at = new_app()
#     at.sidebar.radio[0].set_value("JWT Secret").run()
#     at.selectbox[0].set_value("bytes").run()
#     button(at, "Generate").click().run()
#     assert not at.exception
#     shown = at.code[0].value
#     assert all(c in "0123456789abcdef" for c in shown)

#     at.text_input(key="name_jsg").input("jwt").run()
#     button(at, "Save").click().run()
#     assert saved_items(tmp_data)[0]["password"] == shown


# def test_jwt_toggles_disabled_unless_custom():
#     at = new_app()
#     at.sidebar.radio[0].set_value("JWT Secret").run()
#     at.selectbox[0].set_value("hex").run()
#     toggles = [t for t in at.toggle]
#     assert all(t.disabled for t in toggles)


# # ---------- Saved tab ----------

# def seed(tmp_data, items):
#     tmp_data.write_text(json.dumps(items), encoding="utf-8")


# def test_saved_tab_lists_items(tmp_data):
#     seed(tmp_data, [{"id": "1", "name": "gmail", "password": "abc",
#                      "date": "2024-01-01 10:00", "type": "rpg"}])
#     at = new_app()
#     assert any("gmail" in e.label for e in at.expander)


# def test_search_by_name_filters(tmp_data):
#     seed(tmp_data, [
#         {"id": "1", "name": "gmail", "password": "a", "date": "d", "type": "rpg"},
#         {"id": "2", "name": "bank", "password": "b", "date": "d", "type": "rpg"},
#     ])
#     at = new_app()
#     at.text_input[1].input("gm").run()  # ورودی جست‌وجو
#     labels = [e.label for e in at.expander]
#     assert any("gmail" in l for l in labels)
#     assert not any("bank" in l for l in labels)


# def test_delete_requires_confirmation(tmp_data):
#     seed(tmp_data, [{"id": "1", "name": "x", "password": "p",
#                      "date": "d", "type": "rpg"}])
#     at = new_app()
#     button(at, "Delete").click().run()
#     assert len(saved_items(tmp_data)) == 1  # بدون تأیید حذف نمی‌شود


# def test_delete_with_confirmation_removes_item(tmp_data):
#     seed(tmp_data, [{"id": "1", "name": "x", "password": "p",
#                      "date": "d", "type": "rpg"}])
#     at = new_app()
#     at.checkbox[0].check().run()
#     button(at, "Delete").click().run()
#     assert saved_items(tmp_data) == []


# def test_change_name_updates_file(tmp_data):
#     seed(tmp_data, [{"id": "1", "name": "old", "password": "p",
#                      "date": "d", "type": "rpg"}])
#     at = new_app()
#     at.text_input(key="n_1").input("new").run()
#     button(at, "Change name").click().run()
#     assert saved_items(tmp_data)[0]["name"] == "new"
