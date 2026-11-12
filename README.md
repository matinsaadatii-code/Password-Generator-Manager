# Password Generator

**Programmer:** Matin Saadatii

- **LinkedIn:** [Matin Saadatii](https://www.linkedin.com/in/matin-saadatii/)
- **Website:** [matechs.ir](https://matechs.ir)
- **Telegram:** [@sMATINss](https://t.me/sMATINss)

## Description

A command-line password generator built with Python.

This project generates random passwords, numeric PIN codes, and JWT secret keys using Python's `secrets` module. It also provides functionality to save, search, list, edit, and delete generated values.

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

### JWT Secret Generation

- Generate secret keys for signing JSON Web Tokens.
- Customize the length (in bits).
- Choose the output encoding: `hex`, `urlsafe`, `bytes`, or `custom`.
- The `custom` encoding supports letters, with optional numbers and symbols.

### Memorable Password Generation

- A memorable password generator is planned.
- The implementation is currently under development.

### Password Management

- Save generated passwords, PIN codes, and JWT secrets.
- Assign a custom name to each saved item.
- Search saved items by name, ID, or value.
- Display saved items.
- Edit existing records.
- Generate a new value for an existing record.
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
| `pass_classes.py` | Generator classes: `RandomPasswordGenerator`, `MemorablePasswordGenerator`, `PinCodeGenerator`, `JWTSecretGenerator`, and the abstract base class `PasswordGenerator`. |
| `helpers.py` | JSON file handling, timestamps, and data management utilities. |
| `main_functions.py` | Search, list, edit, and delete operations. |
| `data.json` | Stores saved passwords, PIN codes, and JWT secrets. |
| `.env` | Contains environment-specific configuration, such as the data file path. |

## Requirements

- Python 3.10 or newer (for the type annotation syntax used in the project, such as `str | bytes` and `list[str]`).
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
python main.py
```

The main menu provides the following options:

```text
==Password Generator==
1. Random Password Generator (RPG)
2. Memorable Password Generator (MPG)
3. Pin Code Generator (PCG)
4. JWT Secret Generator (JSG)
5. Exit
--------------------------------------------------
```

### 1. Random Password Generator (RPG)

The random password generator allows you to:

- Enable numbers.
- Enable special characters.
- Change password length.
- Display the generated password.
- Save the password.
- Search, list, edit, and delete saved passwords.

### 2. Memorable Password Generator (MPG)

This feature is currently under development and is not fully available. The menu includes options for capitalization, separator, and number of words, but the generator is not complete.

### 3. Pin Code Generator (PCG)

The PIN code generator allows you to:

- Change PIN length.
- Generate a numeric PIN.
- Save the PIN.
- Search, list, edit, and delete saved PIN codes.

### 4. JWT Secret Generator (JSG)

The JWT secret generator allows you to:

- Enable numbers and symbols (for the `custom` encoding).
- Change the secret length in bits.
- Change the encoding (`hex`, `urlsafe`, `bytes`, or `custom`).
- Display the generated secret.
- Save the secret.
- Search, list, edit, and delete saved JWT secrets.

For HMAC-SHA256 signing, use at least 256 bits (`length = 256`), as recommended by RFC 7518.

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

The `type` field identifies the record category:

| Type | Description |
|---|---|
| `RPG` | Random Password Generator |
| `MPG` | Memorable Password Generator |
| `PCG` | PIN Code Generator |
| `JWT` | JWT Secret Generator |

Each record receives a unique ID generated using Python's `uuid` module.

## Technologies

- **Python**: Main programming language.
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

## License

This project is currently available for educational and personal use. A license can be added to the repository to specify its reuse and distribution terms.

---

**Developed by Matin Saadatii**
