import secrets
import string
import nltk
from abc import ABC, abstractmethod


# data
# nltk.download("words")


class PasswordGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self) -> str:
        pass


class RandomPasswordGenerator(PasswordGenerator):
    def __init__(self, length: int = 8, include_numbers: bool = False, include_symbols: bool = False):
        self.length: int = length

        self.include_numbers: bool = include_numbers
        self.include_symbols: bool = include_symbols

    @property
    def characters(self) -> str:
        chars = string.ascii_letters
        if self.include_numbers:
            chars += string.digits
        if self.include_symbols:
            chars += string.punctuation
        return chars

    def generate(self) -> str:
        chars = self.characters
        return ''.join([secrets.choice(chars) for _ in range(self.length)])


# class MemorablePasswordGenerator(PasswordGenerator):
#     def __init__(self, no_of_words: int = 5, separator: str = '-', capitalization: bool = False, vocabulary: Optional[list[str]] = None):
#         if vocabulary is None:
#             if capitalization:
#                 vocabulary = [secrets.choice(words.words()).capitalize()]

#             vocabulary = [secrets.choice(words.words())]

#         self.no_of_words: int = no_of_words
#         self.separator: str = separator
#         self.capitalization: bool = capitalization
#         self.vocabulary: list[str] = vocabulary

#     def generate(self) -> str:
#         return self.separator.join(secrets.choice(self.vocabulary) for _ in range(self.no_of_words))


class PinCodeGenerator(PasswordGenerator):
    def __init__(self, length: int = 8):
        self.length: int = length

    def generate(self) -> str:
        return ''.join([secrets.choice(string.digits) for _ in range(self.length)])
