"""
Streamlit web interface for the Password / PIN / JWT Secret Generator.

This module builds a single-page Streamlit application that lets the user:

* choose a generator type from the sidebar,
* configure it and generate a new value (*Generate* tab),
* save the generated value under a custom name,
* search, list, rename, edit, regenerate, and delete saved items
  (*Saved* tab).

The generator classes live in :mod:`pass_classes`, persistence helpers
(load/save JSON records) live in :mod:`helpers`, and record update
helpers live in :mod:`main_functions`.

Run with::

    streamlit run app.py

:Dependencies:
    * ``streamlit``
    * ``pass_classes``, ``helpers``, ``main_functions`` (project modules)

.. note::
    The type identifiers in ``TYPES`` must match the ``type`` values used
    when records are saved (``RPG``, ``MPG``, ``PCG``, ``JWT``). See the
    *Notes* section below.
"""

import streamlit as st
import pass_classes, helpers, main_functions

# Page title shown at the top of the app.
st.title("Password/Pin/JWT Secret Generator")

# Maps the label shown in the sidebar to the internal record type.
# Keys   : human-readable labels (shown in the radio button).
# Values : internal type identifiers used for storage and comparisons.
TYPES = {
    "Random Password": "RPG",
    "Memorable Password": "MPG",
    "Pin Code": "PCG",
    "JWT Secret": "JWT",
}

# Sidebar radio that selects which generator is active.
option = st.sidebar.radio("Select Password type:", list(TYPES))
ptype = TYPES[option]


def to_text(value) -> str:
    """Convert a generator output into a string suitable for display and storage.

    :param value: The value returned by ``generator.generate()``. It can be
        a ``str`` or ``bytes``.
    :type value: str | bytes
    :return: The value as a string. ``bytes`` are converted to a hexadecimal
        string; ``str`` values are returned unchanged.
    :rtype: str
    """
    return value.hex() if isinstance(value, bytes) else value


# Two tabs: one to generate new values, one to manage saved values.
tab_gen, tab_saved = st.tabs(["Generate", "Saved"])

# ============ Generator settings (Generate tab) ============
with tab_gen:
    # Each branch shows the controls for one generator type and
    # creates the matching generator object ``generator``.
    if ptype == "RPG":
        # Password length, 1 to 1000 characters, default 12.
        length = st.slider("Select length:", 1, 1000, 12)
        # Whether to include symbols and digits in the password.
        sym = st.toggle("Include Symbols")
        num = st.toggle("Include Numbers")
        generator = pass_classes.RandomPasswordGenerator(
            length=length, include_numbers=num, include_symbols=sym)

    elif ptype == "MPG":
        # Number of words, 1 to 100, default 4.
        words = st.slider("Select number of words:", 1, 100, 4)
        # Text placed between words, up to 10 characters, default "_".
        sep = st.text_input("Separator:", value="_", max_chars=10)
        # Whether to capitalize the words.
        cap = st.toggle("Capitalization")
        generator = pass_classes.MemorablePasswordGenerator(
            number_of_words=words, separator=sep, capitalization=cap)

    elif ptype == "PCG":
        # PIN length, 1 to 100 digits, default 4.
        length = st.slider("Select length:", 1, 100, 4)
        generator = pass_classes.PinCodeGenerator(length=length)

    else:  # JWT
        # Secret length in bits, 8 to 512, step 8, default 256.
        length = st.slider("Select length (bits):", 8, 512, 256, step=8)
        encoding = st.selectbox("Encoding:", ["hex", "urlsafe", "bytes", "custom"])
        # Symbols and numbers only apply to the "custom" encoding,
        # so the toggles are disabled for other encodings.
        custom = encoding == "custom"
        sym = st.toggle("Include Symbols", disabled=not custom)
        num = st.toggle("Include Numbers", disabled=not custom)
        generator = pass_classes.JWTSecretGenerator(
            length=length, encoding=encoding,
            include_numbers=num, include_symbols=sym)

    # Session-state key for the last generated value of this type.
    # Keeping one key per type prevents values from leaking between types.
    key = f"password_{ptype}"

    if st.button("Generate", type="primary"):
        try:
            st.session_state[key] = to_text(generator.generate())
        except ValueError as e:
            # Generators raise ValueError for invalid settings.
            st.error(str(e))

    # Show the last generated value, if any, with a save form.
    password = st.session_state.get(key)
    if password:
        st.code(password)
        name = st.text_input("Enter your Password name:", max_chars=50,
                             placeholder="test", key=f"name_{ptype}")
        if st.button("Save"):
            if not name.strip():
                st.warning("Name can't be empty.")
            else:
                helpers.save_item(name.strip(), password, ptype)
                st.success("Password saved successfully!")

# ============ Search / List / Edit / Delete (Saved tab) ============
with tab_saved:
    # Load only the records that match the selected type.
    items = helpers.get_items_by_type(ptype)

    # Search mode: match by name (case-insensitive substring),
    # by exact ID, or by exact value.
    mode = st.radio("Search by:", ["Name", "Id", "Password/Pin"], horizontal=True)
    query = st.text_input("Search (leave empty to list all):")

    if query:
        if mode == "Name":
            items = [i for i in items if query.strip().lower() in i["name"].lower()]
        elif mode == "Id":
            items = [i for i in items if i["id"] == query.strip()]
        else:
            items = [i for i in items if i["password"] == query]

    if not items:
        st.info("Not found." if query else "There are no saved items yet.")
    else:
        st.caption(f"Found {len(items)} item(s)")

    # Render one expander per record with its actions.
    for item in items:
        iid = item["id"]
        with st.expander(f'{item["name"]} — {item["date"]}'):
            st.code(item["password"])
            # Show the ID, and the last update time if the record has one.
            st.caption(f"ID: {iid}"
                       + (f' | Updated: {item["updated"]}' if item.get("updated") else ""))

            # --- Rename the record ---
            new_name = st.text_input("New name", value=item["name"], key=f"n_{iid}")
            if st.button("Change name", key=f"bn_{iid}"):
                if new_name.strip():
                    main_functions.update_item(iid, name=new_name.strip())
                    st.rerun()
                else:
                    st.warning("Name can't be empty.")

            # --- Manually set a new value ---
            new_value = st.text_input("New password/pin", key=f"p_{iid}")
            if st.button("Change value", key=f"bp_{iid}"):
                if new_value:
                    main_functions.update_item(iid, password=new_value)
                    st.rerun()
                else:
                    st.warning("Value can't be empty.")

            # --- Generate a new value using the Generate tab's settings ---
            if st.button("Generate a new one", key=f"bg_{iid}"):
                try:
                    main_functions.update_item(iid, password=to_text(generator.generate()))
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

            # --- Delete with confirmation ---
            # The delete button stays disabled until the checkbox is ticked.
            confirm = st.checkbox("Confirm delete", key=f"c_{iid}")
            if st.button("Delete", key=f"bd_{iid}", disabled=not confirm):
                # Rewrite the file without the record that has this ID.
                helpers.save_items(
                    [i for i in helpers.load_items() if i.get("id") != iid])
                st.rerun()
