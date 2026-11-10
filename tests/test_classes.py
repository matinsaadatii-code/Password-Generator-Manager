import string

import pytest

from src.pass_classes import (
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
# MemorablePasswordGenerator (unfinished in the source)
# ====================================================

@pytest.mark.skip(reason="MemorablePasswordGenerator is still under development")
class TestMemorablePasswordGenerator:
    def test_placeholder(self):
        pass