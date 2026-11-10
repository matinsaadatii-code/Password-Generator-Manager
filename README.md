# Password Generator

**Programmer:** Matin Saadatii

- **LinkedIn:** [Matin Saadatii](https://www.linkedin.com/in/matin-saadatii/)
- **Website:** [matechs.ir](https://matechs.ir)
- **Telegram:** [@sMATINss](https://t.me/sMATINss)

## Description

A command-line password generator built with Python.

This project allows users to generate random passwords and PIN codes using Python's secure random number generator. It also provides functionality to save, search, edit, and delete generated credentials.

The project is designed with an object-oriented structure and separates password generation, data management, and application logic into different modules.

## Features

### Password Generation

- Generate random passwords.
- Customize password length.
- Include or exclude numbers.
- Include or exclude special characters.
- Use Python's `secrets` module for secure random selection.

### PIN Code Generation

- Generate numeric PIN codes.
- Customize PIN length.
- Use secure random selection instead of the standard `random` module.

### Memorable Password Generation

- A memorable password generator is planned.
- The implementation is currently under development.

### Password Management

- Save generated passwords and PIN codes.
- Assign a custom name to each saved item.
- Search saved items by name, ID, or password/PIN.
- Display saved items.
- Edit existing records.
- Generate a new password or PIN for an existing record.
- Delete saved records.
- Store records in a JSON file.

## Project Structure

```text
Password-Generator/
│
├── main.py
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
| `main.py` | Application entry point and command-line menus. |
| `pass_classes.py` | Password generator classes and generation algorithms. |
| `helpers.py` | JSON file handling, timestamps, and data management utilities. |
| `main_functions.py` | Search, list, edit, update, and delete operations. |
| `data.json` | Stores saved passwords and PIN codes. |
| `.env` | Contains environment-specific configuration, such as the data file path. |

## Requirements

- Python 3.10 or newer (for the type annotation syntax used in the project).
- Required Python packages:
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
pip install python-dotenv nltk
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
python main.py
```

The main menu provides the following options:

```text
==Password Generator==

1. Random Password Generator
2. Memorable Password Generator
3. Pin Code Generator
4. Exit
```

### 1. Random Password Generator

The random password generator allows you to:

- Enable or disable numbers.
- Enable or disable special characters.
- Change password length.
- Display the generated password.
- Save the password.
- Search, list, edit, and delete saved passwords.

### 2. Memorable Password Generator

This feature is currently under development and is not fully available.

### 3. PIN Code Generator

The PIN code generator allows you to:

- Change PIN length.
- Generate a numeric PIN.
- Save the PIN.
- Search, list, edit, and delete saved PIN codes.

## Data Storage

Saved passwords and PIN codes are stored as JSON records.

A record has the following structure:

```json
{
    "name": "My Account",
    "password": "Example123!",
    "date": "2026-11-10 12:30:00",
    "type": "RPG",
    "id": "unique-record-id"
}
```

The `type` field identifies the record category:

| Type | Description |
|---|---|
| `RPG` | Random Password Generator |
| `MPG` | Memorable Password Generator |
| `PCG` | PIN Code Generator |

Each record receives a unique ID generated using Python's `uuid` module.

## Technologies

- **Python** — Main programming language.
- **OOP** — Object-oriented programming and abstract classes.
- **Secrets** — Cryptographically strong random selection.
- **JSON** — Data serialization and storage.
- **UUID** — Unique record identifiers.
- **Python-dotenv** — Environment variable management.
- **NLTK** — Planned use for memorable password generation.

## Security Notes

This project is intended for learning and personal experimentation. It is not a production-ready password manager.

**Important security considerations:**

- Saved passwords and PIN codes are currently stored in plain text inside a JSON file.
- Anyone who can access that file may be able to read the saved credentials.
- Do not use this project to store real or sensitive account passwords.
- Avoid committing `.env` files or generated credential data to a public repository.
- The `secrets` module provides secure random generation, but it does not encrypt stored data.

## Future Improvements

- [ ] Complete the memorable password generator.
- [ ] Add password strength evaluation.
- [ ] Add stronger data protection and encrypted storage.
- [ ] Improve input validation and error handling.
- [ ] Add unit tests.
- [ ] Add a graphical user interface.
- [ ] Add export and import functionality.
- [ ] Improve the user experience and command-line interface.

## License

This project is currently available for educational and personal use. A license can be added to the repository to specify its reuse and distribution terms.

---

**Developed by Matin Saadatii**