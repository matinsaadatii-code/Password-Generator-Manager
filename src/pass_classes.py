"""
Password, PIN, and Secret Generator Classes
===========================================

This module provides classes for generating random passwords,
numeric PIN codes, and secret keys suitable for JSON Web Token
(JWT) signing.

Classes
-------

:class:`PasswordGenerator`
    Abstract base class that defines the common interface for all
    generators.

:class:`RandomPasswordGenerator`
    Generates random passwords from configurable character groups.

:class:`MemorablePasswordGenerator`
    Generates passphrases by joining randomly selected dictionary
    words. This class is under development.

:class:`PinCodeGenerator`
    Generates numeric PIN codes.

:class:`JWTSecretGenerator`
    Generates secret keys for signing JSON Web Tokens.

Security
--------

All random values are produced with the :mod:`secrets` module,
which is designed for cryptographically strong randomness. The
:mod:`random` module is intentionally not used.

Dependencies
------------

- :mod:`secrets` (standard library)
- :mod:`string` (standard library)
- :mod:`math` (standard library)
- :mod:`abc` (standard library)
- :mod:`typing` (standard library)
- `nltk <https://www.nltk.org/>`_ (required by
  :class:`MemorablePasswordGenerator` when no custom vocabulary
  is supplied)

Setup
-----

Download the NLTK ``words`` corpus once during project setup::

    import nltk
    nltk.download("words")

Example
-------

.. code-block:: python

    from password_generator import RandomPasswordGenerator, PinCodeGenerator

    password = RandomPasswordGenerator(
        length=16,
        include_numbers=True,
        include_symbols=True,
    ).generate()

    pin = PinCodeGenerator(length=6).generate()
"""

import secrets
import string
import nltk
import math

from abc import ABC, abstractmethod
from typing import Optional


# ============================================================
# DATA AND DEPENDENCIES
# ============================================================

# Download the NLTK words corpus before using
# MemorablePasswordGenerator with the default vocabulary.
#
# Execute this command once during project setup:
# nltk.download("words")


# ============================================================
# ABSTRACT BASE CLASS
# ============================================================

class PasswordGenerator(ABC):
    """
    Abstract base class for password, PIN, and secret generators.

    This class defines the common interface that all generator
    classes in this module implement. It cannot be instantiated
    directly.

    Subclasses must implement the :meth:`generate` method.

    :raises TypeError: If an attempt is made to instantiate
        this abstract class directly.

    Example of a subclass::

        class HexGenerator(PasswordGenerator):
            def generate(self) -> str:
                return secrets.token_hex(8)
    """

    @abstractmethod
    def generate(self) -> str:
        """
        Generate and return a password, PIN, or secret.

        This abstract method must be implemented by subclasses.

        :return: The generated value.
        :rtype: str
        """
        pass


# ============================================================
# RANDOM PASSWORD GENERATOR
# ============================================================

class RandomPasswordGenerator(PasswordGenerator):
    """
    Generate random passwords from configurable character groups.

    By default, generated passwords contain only uppercase and
    lowercase English letters. Digits and punctuation characters
    can optionally be added.

    :param length: Number of characters in the generated password.
        Defaults to ``8``.
    :type length: int

    :param include_numbers: Whether digit characters (``0-9``)
        should be included in the password. Defaults to ``False``.
    :type include_numbers: bool

    :param include_symbols: Whether punctuation characters
        should be included in the password. Defaults to ``False``.
    :type include_symbols: bool

    :ivar length: Configured password length.
    :vartype length: int

    :ivar include_numbers: Indicates whether digits are enabled.
    :vartype include_numbers: bool

    :ivar include_symbols: Indicates whether symbols are enabled.
    :vartype include_symbols: bool

    :raises ValueError: If ``length`` is less than ``1``.

    Example::

        gen = RandomPasswordGenerator(length=12, include_numbers=True)
        password = gen.generate()
    """

    def __init__(
        self,
        length: int = 8,
        include_numbers: bool = False,
        include_symbols: bool = False
    ) -> None:
        """
        Initialize the random password generator.

        :param length: Desired password length. Defaults to ``8``.
        :type length: int

        :param include_numbers: Enable digit characters if ``True``.
            Defaults to ``False``.
        :type include_numbers: bool

        :param include_symbols: Enable punctuation characters if
            ``True``. Defaults to ``False``.
        :type include_symbols: bool

        :raises ValueError: If the specified length is less than ``1``.
        """

        if length < 1:
            raise ValueError("Password length must be at least 1.")

        # Store the password configuration.
        self.length: int = length
        self.include_numbers: bool = include_numbers
        self.include_symbols: bool = include_symbols

    @property
    def characters(self) -> str:
        """
        Return the character pool used for password generation.

        ASCII letters are always included. Digits and punctuation
        are added according to the generator's configuration.

        :return: A string containing all available characters.
        :rtype: str
        """

        # Start with uppercase and lowercase English letters.
        chars: str = string.ascii_letters

        # Add digits if enabled.
        if self.include_numbers:
            chars += string.digits

        # Add punctuation characters if enabled.
        if self.include_symbols:
            chars += string.punctuation

        return chars

    def generate(self) -> str:
        """
        Generate a random password using the current configuration.

        Characters are selected independently and uniformly from
        :attr:`characters` until :attr:`length` characters have been
        chosen.

        :return: A randomly generated password of length
            :attr:`length`.
        :rtype: str

        .. note::
            :func:`secrets.choice` is used instead of
            :func:`random.choice` because it is designed for
            security-sensitive random generation.
        """

        # Get the currently available character pool.
        chars: str = self.characters

        # Select random characters until the desired length is reached.
        return ''.join(
            secrets.choice(chars)
            for _ in range(self.length)
        )


# ============================================================
# MEMORABLE PASSWORD GENERATOR (UNDER DEVELOPMENT)
# ============================================================

class MemorablePasswordGenerator(PasswordGenerator):
    """
    Generate memorable passphrases from randomly selected words.

    This generator joins several dictionary words with a
    configurable separator. Passphrases are easier to remember than
    random character strings of similar strength.

    .. warning::
        This class is under development and its interface may change.

    :param number_of_words: Number of words used in the passphrase.
        Defaults to ``4``.
    :type number_of_words: int

    :param separator: String placed between selected words.
        Defaults to ``'-'``.
    :type separator: str

    :param capitalization: Capitalize each selected word if ``True``.
        Defaults to ``False``.
    :type capitalization: bool

    :param vocabulary: Custom list of words. If ``None``, the NLTK
        ``words`` corpus is used. Defaults to ``None``.
    :type vocabulary: list[str] or None

    :ivar number_of_words: Configured number of words.
    :vartype number_of_words: int

    :ivar separator: Word separator.
    :vartype separator: str

    :ivar capitalization: Capitalization setting.
    :vartype capitalization: bool

    :ivar vocabulary: Words available for passphrase generation.
    :vartype vocabulary: list[str]

    :raises LookupError: If ``vocabulary`` is ``None`` and the NLTK
        ``words`` corpus has not been downloaded.

    Example::

        gen = MemorablePasswordGenerator(
            number_of_words=3,
            separator=' ',
            capitalization=True,
            vocabulary=['correct', 'horse', 'battery', 'staple'],
        )
        passphrase = gen.generate()
    """

    def __init__(
        self,
        number_of_words: int = 4,
        separator: str = '-',
        capitalization: bool = False,
        vocabulary: Optional[list[str]] = None
    ) -> None:
        """
        Initialize the memorable passphrase generator.

        :param number_of_words: Number of words to combine.
            Defaults to ``4``.
        :type number_of_words: int

        :param separator: Separator placed between selected words.
            Defaults to ``'-'``.
        :type separator: str

        :param capitalization: Capitalize each selected word if
            ``True``. Defaults to ``False``.
        :type capitalization: bool

        :param vocabulary: Custom vocabulary, or ``None`` to use the
            NLTK ``words`` corpus. Defaults to ``None``.
        :type vocabulary: list[str] or None

        :raises LookupError: If ``vocabulary`` is ``None`` and the
            NLTK ``words`` corpus is not installed.
        """

        if vocabulary is None:
            vocabulary = nltk.corpus.words.words()

        self.number_of_words: int = number_of_words
        self.separator: str = separator
        self.capitalization: bool = capitalization
        self.vocabulary: list[str] = vocabulary

    def generate(self) -> str:
        """
        Generate a passphrase from randomly selected words.

        Each word is chosen independently and uniformly from
        :attr:`vocabulary`. If :attr:`capitalization` is enabled,
        each word is capitalized before joining.

        :return: A passphrase made of :attr:`number_of_words` words
            joined by :attr:`separator`.
        :rtype: str

        .. note::
            :func:`secrets.choice` is used for secure selection.
        """

        return self.separator.join(
            secrets.choice(self.vocabulary).capitalize()
            if self.capitalization
            else secrets.choice(self.vocabulary)
            for _ in range(self.number_of_words)
        )


# ============================================================
# PIN CODE GENERATOR
# ============================================================

class PinCodeGenerator(PasswordGenerator):
    """
    Generate numeric PIN codes of a configurable length.

    PIN codes contain only decimal digits (``0-9``).

    :param length: Number of digits in the generated PIN.
        Defaults to ``8``.
    :type length: int

    :ivar length: Configured PIN length.
    :vartype length: int

    :raises ValueError: If ``length`` is less than ``1``.

    .. note::
        PIN codes are returned as strings rather than integers
        so that leading zeros are preserved.

    Example::

        pin = PinCodeGenerator(length=4).generate()  # e.g. '0372'
    """

    def __init__(self, length: int = 8) -> None:
        """
        Initialize the PIN code generator.

        :param length: Desired PIN length. Defaults to ``8``.
        :type length: int

        :raises ValueError: If the specified length is less than ``1``.
        """

        if length < 1:
            raise ValueError("PIN length must be at least 1.")

        # Store the desired PIN length.
        self.length: int = length

    def generate(self) -> str:
        """
        Generate a random numeric PIN code.

        Digits are selected independently and uniformly from
        ``0-9`` until :attr:`length` digits have been chosen.

        :return: A randomly generated PIN of :attr:`length` digits.
        :rtype: str

        .. note::
            The result is a string, not an integer, so leading
            zeros are preserved.
        """

        return ''.join(
            secrets.choice(string.digits)
            for _ in range(self.length)
        )


# ============================================================
# JWT SECRET GENERATOR
# ============================================================

class JWTSecretGenerator(PasswordGenerator):
    """
    Generate random secret keys suitable for JWT signing.

    The output format is selected with :attr:`encoding`:

    - ``'hex'``: hexadecimal string from :func:`secrets.token_hex`.
    - ``'urlsafe'``: URL-safe Base64 string from
      :func:`secrets.token_urlsafe`.
    - ``'bytes'``: raw bytes from :func:`secrets.token_bytes`.
    - ``'custom'``: string drawn from ASCII letters, and optionally
      digits and punctuation, as set by :attr:`include_numbers` and
      :attr:`include_symbols`.

    :param length: Desired entropy in **bits**. Defaults to ``32``.
        For the ``'hex'``, ``'urlsafe'``, and ``'bytes'`` encodings,
        the number of random bytes is ``length // 8``.
    :type length: int

    :param encoding: Output format. One of ``'hex'``, ``'urlsafe'``,
        ``'bytes'``, or ``'custom'``. Defaults to ``'hex'``.
    :type encoding: str

    :param include_numbers: Include digits in the ``'custom'``
        character pool. Ignored for other encodings.
        Defaults to ``True``.
    :type include_numbers: bool

    :param include_symbols: Include punctuation in the ``'custom'``
        character pool. Ignored for other encodings.
        Defaults to ``False``.
    :type include_symbols: bool

    :ivar length: Configured secret length in bits.
    :vartype length: int

    :ivar encoding: Configured output format.
    :vartype encoding: str

    :ivar include_numbers: Indicates whether digits are enabled
        for the ``'custom'`` encoding.
    :vartype include_numbers: bool

    :ivar include_symbols: Indicates whether symbols are enabled
        for the ``'custom'`` encoding.
    :vartype include_symbols: bool

    :raises ValueError: If ``length`` is less than ``1``.

    .. note::
        Use at least 256 bits (``length=256``) for HMAC-SHA256 JWT
        signing keys, as recommended by RFC 7518, section 3.2.

    Example::

        secret = JWTSecretGenerator(length=256).generate()
    """

    def __init__(
        self,
        length: int = 32,
        encoding: str = 'hex',
        include_numbers: bool = True,
        include_symbols: bool = False
    ) -> None:
        """
        Initialize the JWT secret generator.

        :param length: Desired entropy in bits. Defaults to ``32``.
        :type length: int

        :param encoding: Output format: ``'hex'``, ``'urlsafe'``,
            ``'bytes'``, or ``'custom'``. Defaults to ``'hex'``.
        :type encoding: str

        :param include_numbers: Include digits in the ``'custom'``
            pool. Defaults to ``True``.
        :type include_numbers: bool

        :param include_symbols: Include punctuation in the
            ``'custom'`` pool. Defaults to ``False``.
        :type include_symbols: bool

        :raises ValueError: If the specified length is less than ``1``.
        """

        if length < 1:
            raise ValueError("Secret length must be at least 1.")

        # Store the desired secret length and output format.
        self.length: int = length
        self.encoding: str = encoding
        self.include_numbers: bool = include_numbers
        self.include_symbols: bool = include_symbols

    @property
    def characters(self) -> str:
        """
        Return the character pool used by the ``'custom'`` encoding.

        ASCII letters are always included. Digits and punctuation
        are added only when :attr:`encoding` is ``'custom'`` and the
        corresponding flags are enabled. For all other encodings the
        pool contains only ASCII letters and is not used.

        :return: A string containing the available characters.
        :rtype: str
        """

        # Start with uppercase and lowercase English letters.
        chars: str = string.ascii_letters

        if self.encoding == 'custom':
            # Add digits if enabled.
            if self.include_numbers:
                chars += string.digits

            # Add punctuation characters if enabled.
            if self.include_symbols:
                chars += string.punctuation

        return chars

    def generate(self) -> str | bytes:
        """
        Generate a random secret for JWT signing.

        The return type depends on :attr:`encoding`:

        - ``'hex'``, ``'urlsafe'``, ``'custom'``: returns :class:`str`.
        - ``'bytes'``: returns :class:`bytes`.

        :return: The generated secret.
        :rtype: str or bytes

        :raises ValueError: If :attr:`encoding` is not one of
            ``'hex'``, ``'urlsafe'``, ``'bytes'``, or ``'custom'``.

        .. note::
            For the ``'hex'``, ``'urlsafe'``, and ``'bytes'``
            encodings, the length is rounded down to a whole number
            of bytes (``length // 8``).
        """
        n_bytes: int = self.length // 8

        if self.encoding == 'hex':
            return secrets.token_hex(n_bytes)
        elif self.encoding == 'urlsafe':
            return secrets.token_urlsafe(n_bytes)
        elif self.encoding == 'bytes':
            return secrets.token_bytes(n_bytes)
        elif self.encoding == 'custom':
            pool: str = self.characters
            n_chars: int = math.ceil(self.length / math.log2(len(pool)))
            return ''.join(secrets.choice(pool) for _ in range(n_chars))
        else:
            raise ValueError(
                "Invalid encoding. Use 'hex', 'urlsafe', 'bytes' or 'custom'."
            )
