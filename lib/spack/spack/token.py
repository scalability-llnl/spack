# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Generic token support."""
import enum
import json
import re
import sys
from typing import Optional

IS_WINDOWS = sys.platform == "win32"

#: A filename starts either with a "." or a "/" or a "{name}/,
# or on Windows, a drive letter followed by a colon and "\"
# or "." or {name}\
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
if not IS_WINDOWS:
    FILENAME = UNIX_FILENAME
else:
    FILENAME = WINDOWS_FILENAME

#: Values that match this (e.g., variants, flags) can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.-]+$")

#: Regex to strip quotes. Group 2 will be the unquoted string.
STRIP_QUOTES = re.compile(r"^(['\"])(.*)\1$")


def strip_quotes_and_unescape(string: str) -> str:
    """Remove surrounding single or double quotes from string, if present."""
    match = STRIP_QUOTES.match(string)
    if not match:
        return string

    # replace any escaped quotes with bare quotes
    quote, result = match.groups()
    return result.replace(rf"\{quote}", quote)


def quote_if_needed(value: str) -> str:
    """Add quotes around the value if it requires quotes.

    This will add quotes around the value unless it matches ``NO_QUOTES_NEEDED``.

    This adds:
    * single quotes by default
    * double quotes around any value that contains single quotes

    If double quotes are used, we json-escape the string. That is, we escape ``\\``,
    ``"``, and control codes.

    """
    if NO_QUOTES_NEEDED.match(value):
        return value

    return json.dumps(value) if "'" in value else f"'{value}'"


class TokenBase(enum.Enum):
    """Base class for an enum type with a regex value"""

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, regex):
        self.regex = regex

    def __str__(self):
        return f"{self._name_}"


class Token:
    """Represents tokens; generated from input by lexer and fed to parse()."""

    __slots__ = "kind", "value", "start", "end"

    def __init__(
        self, kind: TokenBase, value: str, start: Optional[int] = None, end: Optional[int] = None
    ):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.kind}, {self.value})"

    def __eq__(self, other):
        return (self.kind == other.kind) and (self.value == other.value)
