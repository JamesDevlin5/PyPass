#!/usr/bin/env python

import abc, argparse, string

class CharClass(abc.ABC):
    """A class of characters; an arbitrary grouping of strings."""

    def __init__(self):
        self.state = self.default_state()

    @abc.abstractmethod
    def default_state(self) -> bool:
        """Gets the default state, whether this character class is included by default."""
        return False

    @abc.abstractmethod
    def get_chars(self) -> str:
        """Gets the characters in this group."""
        return ""

    @abc.abstractproperty
    def name(self) -> str:
        """Gets the name of this character group."""
        return "<UNK>"

    @property
    def state(self) -> bool:
        """Gets whether the character class is currently enabled, or included in the final password outcome."""
        return self._state

    @state.setter
    def state(self, new_state: bool):
        """Enabled or disabled this character class, by noting such in the internal state variable."""
        self._state = new_state

class AlphaLower(CharClass):
    """Alphabetical characters, in lowercase."""
    def default_state(self) -> bool:
        return True

    def get_chars(self) -> str:
        return string.ascii_lowercase

    @property
    def name(self) -> str:
        return "Lowercase Alphabetic"

class AlphaUpper(CharClass):
    def default_state(self) -> bool:
        return True

    def get_chars(self) -> str:
        return string.ascii_uppercase

    @property
    def name(self) -> str:
        return "Uppercase Alphabetic"

class NumberDigit(CharClass):
    """Numerical digits."""
    def default_state(self) -> bool:
        return True

    def get_chars(self) -> str:
        return string.digits

    @property
    def name(self) -> bool:
        return "Numerical Digits"

class Symbol(CharClass):
    """Symbolic Characters."""
    def default_state(self) -> bool:
        return False

    def get_chars(self) -> str:
        return string.punctuation

    @property
    def name(self) -> str:
        return "Symbols"

class ClassMgr:
    def __init__(self):
        self._char_classes = []

    def register(self, char_cls: CharClass):
        self._char_classes.append(char_cls)

    def get_all_chars(self) -> str:
        """Gets all characters, from all registered character classes."""
        return ''.join(char_cls.get_chars() for char_cls in self._char_classes if char_cls.state)

    @classmethod
    def default(cls):
        default = cls()
        default.register(AlphaLower())
        default.register(AlphaUpper())
        default.register(NumberDigit())
        default.register(Symbol())
        return default

char_classes = {
        'lower': AlphaLower(),
        'upper': AlphaUpper(),
        'digit': NumberDigit(),
        'symbol': Symbol()
}

def parser():
    par = argparse.ArgumentParser(description='Generates a random, secure password string.')
    for char_cls in char_classes:
        short_id = f"-{char_cls[0]}"
        long_id = f"--{char_cls}"
        par.add_argument(short_id, long_id, action='store_true', dest=char_cls, default=char_classes[char_cls].state, help=f"Enable the Character Class: {char_classes[char_cls].name}.")

    return par

def main():
    args = parser().parse_args()
    mgr = ClassMgr()
    for name, state in vars(args).items():
        if state:
            mgr.register(char_classes[name])
    print(mgr.get_all_chars())

if __name__ == '__main__':
    main()
