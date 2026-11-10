
"""
Password and PIN Generator Classes
==================================

This module provides classes for generating random passwords
and numeric PIN codes.

Classes:
    PasswordGenerator: Abstract base class for all generators.
    RandomPasswordGenerator: Generates random passwords.
    PinCodeGenerator: Generates numeric PIN codes.

The :mod:`secrets` module is used to generate cryptographically
strong random values.

Dependencies:
    - secrets
    - string
    - abc
    - nltk (planned for MemorablePasswordGenerator)
"""

import secrets
import string
import nltk

from abc import ABC, abstractmethod
from typing import Optional


# ============================================================
# DATA AND DEPENDENCIES
# ============================================================

# Download the NLTK words corpus when implementing the
# MemorablePasswordGenerator class.
#
# Execute this command once during project setup:
# nltk.download("words")


# ============================================================
# ABSTRACT BASE CLASS
# ============================================================

class PasswordGenerator(ABC):
    """
    Abstract base class for password and PIN generators.

    This class defines a common interface for all password
    generation classes.

    Subclasses must implement the :meth:`generate` method.

    :raises TypeError: If an attempt is made to instantiate
        this abstract class directly.
    """

    @abstractmethod
    def generate(self) -> str:
        """
        Generate and return a password or PIN.

        This abstract method must be implemented by subclasses.

        :return: The generated password or PIN.
        :rtype: str
        """
        pass


# ============================================================
# RANDOM PASSWORD GENERATOR
# ============================================================

class RandomPasswordGenerator(PasswordGenerator):
    """
    Generate random passwords using configurable character groups.

    By default, generated passwords contain uppercase and
    lowercase English letters.

    Numbers and symbols can optionally be included.

    :param length: Number of characters in the generated password.
        Defaults to ``8``.
    :type length: int

    :param include_numbers: Whether numeric characters should
        be included in the password.
    :type include_numbers: bool

    :param include_symbols: Whether punctuation characters
        should be included in the password.
    :type include_symbols: bool

    :ivar length: Configured password length.
    :vartype length: int

    :ivar include_numbers: Indicates whether numbers are enabled.
    :vartype include_numbers: bool

    :ivar include_symbols: Indicates whether symbols are enabled.
    :vartype include_symbols: bool

    :raises ValueError: If ``length`` is less than ``1``.
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

        :param include_numbers: Enable numeric characters if ``True``.
        :type include_numbers: bool

        :param include_symbols: Enable punctuation characters if ``True``.
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
        Return the available character pool for password generation.

        Letters are always included. Numbers and symbols are added
        according to the generator's configuration.

        :return: A string containing all available characters.
        :rtype: str
        """

        # Start with uppercase and lowercase English letters.
        chars: str = string.ascii_letters

        # Add numeric characters if enabled.
        if self.include_numbers:
            chars += string.digits

        # Add punctuation characters if enabled.
        if self.include_symbols:
            chars += string.punctuation

        return chars

    def generate(self) -> str:
        """
        Generate a random password using the current configuration.

        The method selects random characters from the available
        character pool until the configured password length is reached.

        :return: A randomly generated password.
        :rtype: str

        .. note::
            The :func:`secrets.choice` function is used instead of
            ``random.choice`` because it is designed for
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

# class MemorablePasswordGenerator(PasswordGenerator):
#     """
#     Generate memorable passwords using randomly selected words.
#
#     This generator combines multiple dictionary words using
#     a configurable separator.
#
#     :param no_of_words: Number of words used in the password.
#         Defaults to ``5``.
#     :type no_of_words: int
#
#     :param separator: String used to separate selected words.
#         Defaults to ``'-'``.
#     :type separator: str
#
#     :param capitalization: Whether selected words should be capitalized.
#     :type capitalization: bool
#
#     :param vocabulary: Custom list of words. If ``None``, the
#         NLTK words corpus is used.
#     :type vocabulary: list[str] or None
#
#     :ivar no_of_words: Configured number of words.
#     :vartype no_of_words: int
#
#     :ivar separator: Word separator.
#     :vartype separator: str
#
#     :ivar capitalization: Capitalization setting.
#     :vartype capitalization: bool
#
#     :ivar vocabulary: Available words for password generation.
#     :vartype vocabulary: list[str]
#     """
#
#     def __init__(
#         self,
#         no_of_words: int = 5,
#         separator: str = '-',
#         capitalization: bool = False,
#         vocabulary: Optional[list[str]] = None
#     ) -> None:
#         """
#         Initialize the memorable password generator.
#
#         :param no_of_words: Number of words to combine.
#         :type no_of_words: int
#
#         :param separator: Separator between selected words.
#         :type separator: str
#
#         :param capitalization: Capitalize selected words if enabled.
#         :type capitalization: bool
#
#         :param vocabulary: Custom vocabulary or ``None`` to use NLTK.
#         :type vocabulary: list[str] or None
#         """
#
#         if vocabulary is None:
#             vocabulary = nltk.corpus.words.words()
#
#         self.no_of_words: int = no_of_words
#         self.separator: str = separator
#         self.capitalization: bool = capitalization
#         self.vocabulary: list[str] = vocabulary
#
#     def generate(self) -> str:
#         """
#         Generate a memorable password from randomly selected words.
#
#         :return: A password consisting of randomly selected words.
#         :rtype: str
#         """
#
#         selected_words: list[str] = [
#             secrets.choice(self.vocabulary)
#             for _ in range(self.no_of_words)
#         ]
#
#         # Capitalize selected words if the option is enabled.
#         if self.capitalization:
#             selected_words = [
#                 word.capitalize()
#                 for word in selected_words
#             ]
#
#         return self.separator.join(selected_words)


# ============================================================
# PIN CODE GENERATOR
# ============================================================

class PinCodeGenerator(PasswordGenerator):
    """
    Generate numeric PIN codes of a configurable length.

    PIN codes contain only decimal digits (0-9).

    :param length: Number of digits in the generated PIN.
        Defaults to ``8``.
    :type length: int

    :ivar length: Configured PIN length.
    :vartype length: int

    :raises ValueError: If ``length`` is less than ``1``.

    .. note::
        PIN codes are returned as strings rather than integers
        to preserve leading zeros.
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

        The method selects decimal digits until the configured
        PIN length is reached.

        :return: A randomly generated numeric PIN.
        :rtype: str

        .. note::
            The returned value is a string, not an integer,
            so leading zeros are preserved.
        """

        return ''.join(
            secrets.choice(string.digits)
            for _ in range(self.length)
        )
