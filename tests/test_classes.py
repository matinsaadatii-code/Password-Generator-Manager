import math
import string
import types

import pytest

from src import pass_classes
from src.pass_classes import (
    JWTSecretGenerator,
    MemorablePasswordGenerator,
    PasswordGenerator,
    PinCodeGenerator,
    RandomPasswordGenerator,
    secrets
)


# ====================================================
# PasswordGenerator (abstract base class)
# ====================================================

class TestPasswordGenerator:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            PasswordGenerator()

    def test_subclass_without_generate_cannot_be_instantiated(self):
        class Incomplete(PasswordGenerator):
            pass

        with pytest.raises(TypeError):
            Incomplete()

    def test_subclass_with_generate_works(self):
        class Complete(PasswordGenerator):
            def generate(self):
                return "x"

        assert Complete().generate() == "x"


# ====================================================
# RandomPasswordGenerator
# ====================================================

class TestRandomPasswordGeneratorInit:
    def test_defaults(self):
        g = RandomPasswordGenerator()
        assert g.length == 8
        assert g.include_numbers is False
        assert g.include_symbols is False

    def test_custom_values(self):
        g = RandomPasswordGenerator(12, True, True)
        assert (g.length, g.include_numbers, g.include_symbols) == (12, True, True)

    @pytest.mark.parametrize("bad", [0, -1, -100])
    def test_invalid_length_raises(self, bad):
        with pytest.raises(ValueError):
            RandomPasswordGenerator(length=bad)

    def test_length_one_is_valid(self):
        assert RandomPasswordGenerator(length=1).length == 1


class TestRandomPasswordGeneratorCharacters:
    def test_letters_only_by_default(self):
        assert RandomPasswordGenerator().characters == string.ascii_letters

    def test_with_numbers(self):
        g = RandomPasswordGenerator(include_numbers=True)
        assert g.characters == string.ascii_letters + string.digits

    def test_with_symbols(self):
        g = RandomPasswordGenerator(include_symbols=True)
        assert g.characters == string.ascii_letters + string.punctuation

    def test_with_numbers_and_symbols(self):
        g = RandomPasswordGenerator(include_numbers=True, include_symbols=True)
        assert g.characters == (
            string.ascii_letters + string.digits + string.punctuation
        )

    def test_characters_reflects_later_changes(self):
        g = RandomPasswordGenerator()
        g.include_numbers = True
        assert string.digits in g.characters


class TestRandomPasswordGeneratorGenerate:
    @pytest.mark.parametrize("length", [1, 8, 50, 1000])
    def test_length(self, length):
        assert len(RandomPasswordGenerator(length=length).generate()) == length

    def test_returns_str(self):
        assert isinstance(RandomPasswordGenerator().generate(), str)

    def test_default_only_letters(self):
        pwd = RandomPasswordGenerator(length=500).generate()
        assert all(c in string.ascii_letters for c in pwd)

    def test_numbers_enabled_no_symbols(self):
        pwd = RandomPasswordGenerator(
            length=500, include_numbers=True
        ).generate()
        assert all(c in string.ascii_letters + string.digits for c in pwd)

    def test_symbols_enabled(self):
        g = RandomPasswordGenerator(
            length=500, include_numbers=True, include_symbols=True
        )
        assert all(c in g.characters for c in g.generate())

    def test_two_passwords_differ(self):
        g = RandomPasswordGenerator(length=32, include_numbers=True)
        assert g.generate() != g.generate()

    def test_length_change_after_creation(self):
        g = RandomPasswordGenerator(length=5)
        g.length = 20
        assert len(g.generate()) == 20

    def test_uses_secrets_choice(self, monkeypatch):
        calls = []

        def fake_choice(seq):
            calls.append(seq)
            return "a"

        monkeypatch.setattr(secrets, "choice", fake_choice)
        assert RandomPasswordGenerator(length=4).generate() == "aaaa"
        assert len(calls) == 4
        assert all(c == string.ascii_letters for c in calls)


# ====================================================
# PinCodeGenerator
# ====================================================

class TestPinCodeGenerator:
    def test_default_length(self):
        assert PinCodeGenerator().length == 8

    @pytest.mark.parametrize("bad", [0, -1, -50])
    def test_invalid_length_raises(self, bad):
        with pytest.raises(ValueError):
            PinCodeGenerator(length=bad)

    def test_length_one_is_valid(self):
        assert len(PinCodeGenerator(length=1).generate()) == 1

    @pytest.mark.parametrize("length", [1, 4, 8, 100])
    def test_generated_length(self, length):
        assert len(PinCodeGenerator(length=length).generate()) == length

    def test_returns_str(self):
        assert isinstance(PinCodeGenerator().generate(), str)

    def test_only_digits(self):
        pin = PinCodeGenerator(length=500).generate()
        assert pin.isdigit()
        assert all(c in string.digits for c in pin)

    def test_leading_zero_preserved(self, monkeypatch):
        monkeypatch.setattr(secrets, "choice", lambda s: "0")
        assert PinCodeGenerator(length=4).generate() == "0000"

    def test_uses_digits_pool(self, monkeypatch):
        seen = []

        def fake_choice(seq):
            seen.append(seq)
            return "1"

        monkeypatch.setattr(secrets, "choice", fake_choice)
        PinCodeGenerator(length=3).generate()
        assert seen == [string.digits] * 3

    def test_two_pins_differ(self):
        g = PinCodeGenerator(length=32)
        assert g.generate() != g.generate()

    def test_length_change_after_creation(self):
        g = PinCodeGenerator(length=4)
        g.length = 10
        assert len(g.generate()) == 10


# ====================================================
# MemorablePasswordGenerator
# ====================================================

WORDS = ["apple", "banana", "cherry", "delta", "echo", "fox", "grape"]


class TestMemorablePasswordGenerator:
    # ---------- construction ----------

    def test_is_password_generator(self):
        assert isinstance(
            MemorablePasswordGenerator(vocabulary=WORDS), PasswordGenerator
        )

    def test_defaults(self):
        g = MemorablePasswordGenerator(vocabulary=WORDS)
        assert g.number_of_words == 4
        assert g.separator == "-"
        assert g.capitalization is False
        assert g.vocabulary == WORDS

    def test_custom_values_are_stored(self):
        g = MemorablePasswordGenerator(
            number_of_words=6, separator="_", capitalization=True,
            vocabulary=WORDS,
        )
        assert (g.number_of_words, g.separator, g.capitalization) == (6, "_", True)

    def test_vocabulary_none_uses_nltk_corpus(self, monkeypatch):
        calls = []

        class FakeWords:
            def words(self):
                calls.append(1)
                return ["one", "two"]

        fake_corpus = types.SimpleNamespace(words=FakeWords())
        monkeypatch.setattr(pass_classes.nltk, "corpus", fake_corpus, raising=False)
        g = MemorablePasswordGenerator()
        assert g.vocabulary == ["one", "two"]
        assert calls == [1]

    def test_custom_vocabulary_does_not_touch_nltk(self, monkeypatch):
        class Boom:
            @property
            def words(self):
                raise AssertionError("nltk must not be used")

        monkeypatch.setattr(
            pass_classes.nltk, "corpus", Boom(), raising=False
        )
        MemorablePasswordGenerator(vocabulary=WORDS)

    # ---------- generate ----------

    def test_returns_str(self):
        assert isinstance(MemorablePasswordGenerator(vocabulary=WORDS).generate(), str)

    @pytest.mark.parametrize("n", [1, 2, 4, 10])
    def test_number_of_words(self, n):
        g = MemorablePasswordGenerator(number_of_words=n, vocabulary=WORDS)
        assert len(g.generate().split("-")) == n

    def test_words_come_from_vocabulary(self):
        g = MemorablePasswordGenerator(number_of_words=20, vocabulary=WORDS)
        assert set(g.generate().split("-")) <= set(WORDS)

    @pytest.mark.parametrize("sep", ["-", "_", ".", " ", "::"])
    def test_separator(self, sep):
        g = MemorablePasswordGenerator(
            number_of_words=3, separator=sep, vocabulary=WORDS
        )
        assert len(g.generate().split(sep)) == 3

    def test_empty_separator_joins_words(self, monkeypatch):
        monkeypatch.setattr(secrets, "choice", lambda seq: seq[0])
        g = MemorablePasswordGenerator(
            number_of_words=3, separator="", vocabulary=["ab"]
        )
        assert g.generate() == "ababab"

    def test_single_word_has_no_separator(self):
        g = MemorablePasswordGenerator(number_of_words=1, vocabulary=WORDS)
        assert "-" not in g.generate()

    def test_uses_secrets_choice_once_per_word(self, monkeypatch):
        calls = []

        def fake_choice(seq):
            calls.append(seq)
            return "x"

        monkeypatch.setattr(secrets, "choice", fake_choice)
        g = MemorablePasswordGenerator(number_of_words=5, vocabulary=WORDS)
        assert g.generate() == "x-x-x-x-x"
        assert len(calls) == 5
        assert all(c is g.vocabulary for c in calls)

    def test_deterministic_with_patched_choice(self, monkeypatch):
        it = iter(["apple", "echo", "fox"])
        monkeypatch.setattr(secrets, "choice", lambda seq: next(it))
        g = MemorablePasswordGenerator(number_of_words=3, vocabulary=WORDS)
        assert g.generate() == "apple-echo-fox"

    # ---------- capitalization ----------

    def test_capitalization_on(self):
        g = MemorablePasswordGenerator(
            number_of_words=10, capitalization=True, vocabulary=WORDS
        )
        assert all(w[0].isupper() and w[1:].islower() for w in g.generate().split("-"))

    def test_capitalization_off_keeps_original(self, monkeypatch):
        monkeypatch.setattr(secrets, "choice", lambda seq: seq[0])
        g = MemorablePasswordGenerator(
            number_of_words=2, vocabulary=["hELLo"]
        )
        assert g.generate() == "hELLo-hELLo"

    def test_capitalization_lowercases_rest_of_word(self, monkeypatch):
        # str.capitalize() lowercases the remaining letters.
        monkeypatch.setattr(secrets, "choice", lambda seq: seq[0])
        g = MemorablePasswordGenerator(
            number_of_words=1, capitalization=True, vocabulary=["hELLo"]
        )
        assert g.generate() == "Hello"

    # ---------- changing settings after creation ----------

    def test_change_number_of_words(self):
        g = MemorablePasswordGenerator(number_of_words=2, vocabulary=WORDS)
        g.number_of_words = 6
        assert len(g.generate().split("-")) == 6

    def test_change_separator(self):
        g = MemorablePasswordGenerator(number_of_words=3, vocabulary=WORDS)
        g.separator = "+"
        assert g.generate().count("+") == 2

    def test_toggle_capitalization(self, monkeypatch):
        monkeypatch.setattr(secrets, "choice", lambda seq: seq[0])
        g = MemorablePasswordGenerator(number_of_words=1, vocabulary=["abc"])
        assert g.generate() == "abc"
        g.capitalization = True
        assert g.generate() == "Abc"

    def test_outputs_differ(self):
        vocab = [f"word{i}" for i in range(1000)]
        g = MemorablePasswordGenerator(number_of_words=4, vocabulary=vocab)
        assert g.generate() != g.generate()

    # ---------- edge cases (document current behavior) ----------

    def test_empty_vocabulary_raises_index_error(self):
        g = MemorablePasswordGenerator(vocabulary=[])
        with pytest.raises(IndexError):
            g.generate()

    @pytest.mark.parametrize("n", [0, -1])
    def test_non_positive_word_count_gives_empty_string(self, n):
        g = MemorablePasswordGenerator(number_of_words=n, vocabulary=WORDS)
        assert g.generate() == ""

    @pytest.mark.xfail(
        reason="Unlike the other generators, no validation for "
               "number_of_words < 1 (should raise ValueError)",
        strict=True,
    )
    @pytest.mark.parametrize("n", [0, -1])
    def test_non_positive_word_count_should_raise(self, n):
        with pytest.raises(ValueError):
            MemorablePasswordGenerator(number_of_words=n, vocabulary=WORDS)


# ====================================================
# JWTSecretGenerator
# ====================================================

class TestJWTSecretGenerator:

    # ---------- construction ----------

    def test_is_password_generator(self):
        assert isinstance(JWTSecretGenerator(), PasswordGenerator)

    def test_default_settings(self):
        g = JWTSecretGenerator()
        assert g.length == 32
        assert g.encoding == 'hex'
        assert g.include_numbers is True
        assert g.include_symbols is False

    @pytest.mark.parametrize("length", [0, -8])
    def test_non_positive_length_raises(self, length):
        with pytest.raises(ValueError, match="Secret length must be at least 1."):
            JWTSecretGenerator(length=length)

    # ---------- hex ----------

    def test_hex_length_is_bits_divided_by_four(self):
        # length is treated as bits: 256 bits -> 32 bytes -> 64 hex chars.
        secret = JWTSecretGenerator(length=256, encoding='hex').generate()
        assert len(secret) == 64
        assert all(c in string.hexdigits for c in secret)

    def test_hex_default_length(self):
        assert len(JWTSecretGenerator().generate()) == 8

    @pytest.mark.parametrize("length", [1, 4, 7])
    def test_hex_under_eight_bits_returns_empty_string(self, length):
        # Current behavior: length // 8 == 0 bytes requested.
        assert JWTSecretGenerator(length=length, encoding='hex').generate() == ""

    # ---------- urlsafe ----------

    def test_urlsafe_uses_url_safe_alphabet(self):
        secret = JWTSecretGenerator(length=256, encoding='urlsafe').generate()
        # token_urlsafe(32) -> 43 characters.
        assert len(secret) == 43
        allowed = string.ascii_letters + string.digits + "-_"
        assert all(c in allowed for c in secret)

    # ---------- bytes ----------

    def test_bytes_returns_bytes_of_expected_size(self):
        secret = JWTSecretGenerator(length=256, encoding='bytes').generate()
        assert isinstance(secret, bytes)
        assert len(secret) == 32

    @pytest.mark.parametrize("length", [1, 7])
    def test_bytes_under_eight_bits_returns_empty(self, length):
        assert JWTSecretGenerator(length=length, encoding='bytes').generate() == b""

    # ---------- custom ----------

    def test_custom_default_pool_is_letters_and_digits(self):
        g = JWTSecretGenerator(length=64, encoding='custom')
        assert g.characters == string.ascii_letters + string.digits

    def test_custom_length_in_characters(self):
        g = JWTSecretGenerator(length=64, encoding='custom')
        pool_size = len(g.characters)
        expected = math.ceil(64 / math.log2(pool_size))
        secret = g.generate()
        assert len(secret) == expected
        assert all(c in g.characters for c in secret)

    def test_custom_letters_only(self):
        g = JWTSecretGenerator(
            length=52, encoding='custom',
            include_numbers=False, include_symbols=False
        )
        assert g.characters == string.ascii_letters
        secret = g.generate()
        assert secret.isalpha()

    def test_custom_with_symbols(self):
        g = JWTSecretGenerator(
            length=64, encoding='custom',
            include_numbers=False, include_symbols=True
        )
        assert g.characters == string.ascii_letters + string.punctuation
        assert all(c in g.characters for c in g.generate())

    # ---------- flags are ignored outside 'custom' ----------

    @pytest.mark.parametrize("encoding", ['hex', 'urlsafe', 'bytes'])
    def test_characters_ignore_flags_for_non_custom(self, encoding):
        g = JWTSecretGenerator(
            encoding=encoding, include_numbers=True, include_symbols=True
        )
        assert g.characters == string.ascii_letters

    # ---------- invalid / changed settings ----------

    def test_invalid_encoding_raises_on_generate(self):
        g = JWTSecretGenerator(encoding='base64')
        with pytest.raises(ValueError, match="Invalid encoding"):
            g.generate()

    def test_change_encoding_after_creation(self):
        g = JWTSecretGenerator(length=64)
        g.encoding = 'bytes'
        assert isinstance(g.generate(), bytes)

    def test_change_length_after_creation(self):
        g = JWTSecretGenerator(length=64, encoding='hex')
        g.length = 128
        assert len(g.generate()) == 32

    def test_outputs_differ(self):
        g = JWTSecretGenerator(length=256, encoding='hex')
        assert g.generate() != g.generate()