# Password Generator

**Programmer:** Matin Saadatii

- **LinkedIn:** [Matin Saadatii](https://www.linkedin.com/in/matin-saadatii/)
- **Website:** [matechs.ir](https://matechs.ir)
- **Telegram:** [@sMATINss](https://t.me/sMATINss)

## Description

A web-based password generator built with Python and [Streamlit](https://streamlit.io).

This project generates random passwords, memorable passwords (planned), numeric PIN codes, and JWT secret keys using Python's `secrets` module. Generated values can be saved with a custom name, then searched, listed, renamed, edited, regenerated, and deleted from a browser interface.

The project is designed with an object-oriented structure and separates password generation, data management, and the user interface into different modules.

## Features

### Password Generation

- Generate random passwords.
- Customize password length (1 to 1000 characters).
- Include or exclude numbers.
- Include or exclude symbols.
- Use Python's `secrets` module for secure random selection.

### PIN Code Generation

- Generate numeric PIN codes.
- Customize PIN length (1 to 100 digits).
- Use secure random selection instead of the standard `random` module.

### JWT Secret Generation

- Generate secret keys for signing JSON Web Tokens.
- Customize the length in bits (8 to 512, in steps of 8).
- Choose the output encoding: `hex`, `urlsafe`, `bytes`, or `custom`.
- The `custom` encoding supports letters, with optional numbers and symbols. The number and symbol options are disabled for the other encodings.

### Memorable Password Generation

- A memorable password generator is planned.
- The interface already includes controls for number of words, separator, and capitalization, but the generator is under development.

### Password Management

- Save generated passwords, PIN codes, and JWT secrets with a custom name.
- Search saved items by name (case-insensitive partial match), by ID (exact match), or by value (exact match).
- List all saved items of the selected type.
- Rename existing records.
- Manually set a new value for an existing record.
- Generate a new value for an existing record using the current generator settings.
- Delete saved records, after confirming with a checkbox.
- Store records in a JSON file.

## Graphical User Interface

The application runs in the browser. The interface has three parts:

- **Sidebar:** A radio button list to select the type: *Random Password*, *Memorable Password*, *Pin Code*, or *JWT Secret*.
- **Generate tab:** Settings for the selected type, a **Generate** button, a display of the generated value, and a name field with a **Save** button.
- **Saved tab:** A search area with a *Search by* option (*Name*, *Id*, or *Password/Pin*), a list of saved items of the selected type shown as expandable cards, and per-item actions.

The last generated value is kept for each type while the session is open. Switching types does not mix values between types.

## Project Structure

```text
Password-Generator/
│
├── app.py
├── pass_classes.py
├── helpers.py
├── main_functions.py
├── data.json
├── .env
├── .gitignore
└── README.md
```

### Modules

| File | Description |
|---|---|
| `app.py` | Streamlit web interface: sidebar, Generate tab, and Saved tab. |
| `pass_classes.py` | Generator classes: `RandomPasswordGenerator`, `MemorablePasswordGenerator`, `PinCodeGenerator`, `JWTSecretGenerator`, and the abstract base class `PasswordGenerator`. |
| `helpers.py` | JSON file handling (`load_items`, `save_items`, `save_item`, `get_items_by_type`), timestamps, and data management utilities. |
| `main_functions.py` | Update operations for saved records (`update_item`), used for renaming, changing values, and regenerating. |
| `data.json` | Stores saved passwords, PIN codes, and JWT secrets. |
| `.env` | Contains environment-specific configuration, such as the data file path. |

## Requirements

- Python 3.10 or newer (for the type annotation syntax used in the project, such as `str | bytes` and `list[str]`).
- Required Python packages:
  - `streamlit`
  - `python-dotenv`
  - `nltk` (used by the planned memorable password generator)

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

**2. Navigate to the project directory**

```bash
cd Password-Generator
```

**3. Create a virtual environment (recommended)**

```bash
python -m venv .venv
```

Activate it:

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

**4. Install dependencies**

```bash
pip install streamlit python-dotenv nltk
```

**5. (Optional) Download the NLTK words corpus**

This is only needed for the Memorable Password Generator, which uses the NLTK `words` corpus by default:

```bash
python -c "import nltk; nltk.download('words')"
```

## Configuration

The application uses a `.env` file to configure the location of its JSON data file.

Create a `.env` file in the project root:

```env
DATA_PATH=data.json
```

You can also specify a different path:

```env
DATA_PATH=storage/passwords.json
```

Make sure the destination directory exists before running the application.

If `DATA_PATH` is not defined, the application uses `data.json` by default.

## Usage

Run the application from the project directory:

```bash
streamlit run app.py
```

Streamlit prints a local address (by default `http://localhost:8501`). Open it in your browser.

### Selecting a Type

Use the **Select Password type** radio button in the sidebar to choose a generator. The Generate and Saved tabs update to match the selected type.

### 1. Random Password

In the **Generate** tab:

- Set the length with the **Select length** slider (1 to 1000).
- Turn on **Include Symbols** and/or **Include Numbers**.
- Click **Generate** to create a password.

### 2. Memorable Password

This feature is currently under development. The controls (**Select number of words**, **Separator**, and **Capitalization**) are present, but the generator is not complete.

### 3. Pin Code

In the **Generate** tab:

- Set the number of digits with the **Select length** slider (1 to 100).
- Click **Generate** to create a PIN.

### 4. JWT Secret

In the **Generate** tab:

- Set the length in bits with the **Select length (bits)** slider (8 to 512, default 256).
- Choose an **Encoding**: `hex`, `urlsafe`, `bytes`, or `custom`.
- For the `custom` encoding only, turn on **Include Symbols** and/or **Include Numbers**.
- Click **Generate** to create a secret.

For HMAC-SHA256 signing, use at least 256 bits, as recommended by RFC 7518.

### Saving a Generated Value

After a value is generated, it appears in a code box below the **Generate** button. To save it:

1. Enter a name in **Enter your Password name**. The name cannot be empty.
2. Click **Save**.

### Managing Saved Items

In the **Saved** tab:

1. Optionally, choose a **Search by** option (*Name*, *Id*, or *Password/Pin*) and type a query. Leave the query empty to list all items of the selected type.
2. Click an item to expand it. Each item shows its value, its ID, and its last update time (if it has been updated).
3. Use the actions inside the item:
   - **Change name:** Enter a new name in **New name**, then click **Change name**.
   - **Change value:** Enter a value in **New password/pin**, then click **Change value**.
   - **Generate a new one:** Click **Generate a new one** to replace the value with a new one, using the settings in the **Generate** tab.
   - **Delete:** Tick **Confirm delete**, then click **Delete**. The button stays disabled until the checkbox is ticked.

**Note:** *Generate a new one* uses the settings currently shown in the **Generate** tab, not the settings used when the record was created.

## Data Storage

Saved passwords, PIN codes, and JWT secrets are stored as JSON records.

A record has the following structure:

```json
{
    "name": "My Account",
    "password": "example-value",
    "date": "2026-11-10 12:30:00",
    "type": "RPG",
    "id": "unique-record-id"
}
```

Records that have been changed also contain an `updated` field with the time of the last update.

The `type` field identifies the record category:

| Type | Description |
|---|---|
| `RPG` | Random Password |
| `MPG` | Memorable Password |
| `PCG` | Pin Code |
| `JWT` | JWT Secret |

Each record receives a unique ID generated using Python's `uuid` module.

## Technologies

- **Python**: Main programming language.
- **Streamlit**: Web user interface.
- **OOP**: Object-oriented programming and abstract classes.
- **Secrets**: Cryptographically strong random selection.
- **JSON**: Data serialization and storage.
- **UUID**: Unique record identifiers.
- **Python-dotenv**: Environment variable management.
- **NLTK**: Planned use for memorable password generation.

## Security Notes

This project is intended for learning and personal experimentation. It is not a production-ready password manager.

**Important security considerations:**

- Saved passwords, PIN codes, and JWT secrets are stored in plain text inside a JSON file.
- Anyone who can access that file may be able to read the saved credentials.
- Do not use this project to store real or sensitive account passwords or production signing keys.
- Avoid committing `.env` files or generated credential data to a public repository.
- The `secrets` module provides secure random generation, but it does not encrypt stored data.
- The Streamlit server is intended for local use. If you make it reachable from a network, anyone who can open the page can view and change the saved data.

## License

This project is currently available for educational and personal use. A license can be added to the repository to specify its reuse and distribution terms.

---

**Developed by Matin Saadatii**
