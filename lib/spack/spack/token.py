# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tokens for parsing spec literals

Here is the EBNF grammar for a spec::

    spec          = [name] [node_options] { ^[edge_properties] node } |
                    [name] [node_options] hash |
                    filename

    node          =  name [node_options] |
                     [name] [node_options] hash |
                     filename

    node_options    = [@(version_list|version_pair)] [%compiler] { variant }
    edge_properties = [ { bool_variant | key_value } ]

    hash          = / id
    filename      = (.|/|[a-zA-Z0-9-_]*/)([a-zA-Z0-9-_./]*)(.json|.yaml)

    name          = id | namespace id
    namespace     = { id . }

    variant       = bool_variant | key_value | propagated_bv | propagated_kv
    bool_variant  =  +id |  ~id |  -id
    propagated_bv = ++id | ~~id | --id
    key_value     =  id=id |  id=quoted_id
    propagated_kv = id==id | id==quoted_id

    compiler      = id [@version_list]

    version_pair  = git_version=vid
    version_list  = (version|version_range) [ { , (version|version_range)} ]
    version_range = vid:vid | vid: | :vid | :
    version       = vid

    git_version   = git.(vid) | git_hash
    git_hash      = [A-Fa-f0-9]{40}

    quoted_id     = " id_with_ws " | ' id_with_ws '
    id_with_ws    = [a-zA-Z0-9_][a-zA-Z_0-9-.\\s]*
    vid           = [a-zA-Z0-9_][a-zA-Z_0-9-.]*
    id            = [a-zA-Z0-9_][a-zA-Z_0-9-]*

Identifiers using the <name>=<value> command, such as architectures and
compiler flags, require a space before the name.

There is one context-sensitive part: ids in versions may contain '.', while
other ids may not.

There is one ambiguity: since '-' is allowed in an id, you need to put
whitespace space before -variant for it to be tokenized properly.  You can
either use whitespace, or you can just use ~variant since it means the same
thing.  Spack uses ~variant in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ~ can cause shell
expansion when it is the first character in an id typed on the command line.
"""
import enum
import json
import re
import sys
from typing import Iterator, Match, Optional

from llnl.util.tty import color

from spack.error import SpecSyntaxError

IS_WINDOWS = sys.platform == "win32"
#: Valid name for specs and variants. Here we are not using
#: the previous "w[\w.-]*" since that would match most
#: characters that can be part of a word in any language
IDENTIFIER = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9\-]*)"
DOTTED_IDENTIFIER = rf"(?:{IDENTIFIER}(?:\.{IDENTIFIER})+)"
GIT_HASH = r"(?:[A-Fa-f0-9]{40})"
#: Git refs include branch names, and can contain "." and "/"
GIT_REF = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9./\-]*)"
GIT_VERSION_PATTERN = rf"(?:(?:git\.(?:{GIT_REF}))|(?:{GIT_HASH}))"

NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

HASH = r"[a-zA-Z_0-9]+"

#: A filename starts either with a "." or a "/" or a "{name}/,
# or on Windows, a drive letter followed by a colon and "\"
# or "." or {name}\
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
if not IS_WINDOWS:
    FILENAME = UNIX_FILENAME
else:
    FILENAME = WINDOWS_FILENAME

#: These are legal values that *can* be parsed bare, without quotes on the command line.
VALUE = r"(?:[a-zA-Z_0-9\-+\*.,:=\~\/\\]+)"

#: Variant/flag values that match this can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.-]+$")

#: Quoted values can be *anything* in between quotes, including escaped quotes.
QUOTED_VALUE = r"(?:'(?:[^']|(?<=\\)')*'|\"(?:[^\"]|(?<=\\)\")*\")"

VERSION = r"=?(?:[a-zA-Z0-9_][a-zA-Z_0-9\-\.]*\b)"
VERSION_RANGE = rf"(?:(?:{VERSION})?:(?:{VERSION}(?!\s*=))?)"
VERSION_LIST = rf"(?:{VERSION_RANGE}|{VERSION})(?:\s*,\s*(?:{VERSION_RANGE}|{VERSION}))*"

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

    If double quotes are used, we json-escpae the string. That is, we escape ``\\``,
    ``"``, and control codes.

    """
    if NO_QUOTES_NEEDED.match(value):
        return value

    return json.dumps(value) if "'" in value else f"'{value}'"


class TokenBase(enum.Enum):
    """Base class for an enum type with a regex value"""

    def __new__(cls, *args, **kwargs):
        # See
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, regex):
        self.regex = regex

    def __str__(self):
        return f"{self._name_}"


class TokenType(TokenBase):
    """Enumeration of the different token kinds in the spec grammar.

    Order of declaration is extremely important, since text containing specs is parsed with a
    single regex obtained by ``"|".join(...)`` of all the regex in the order of declaration.
    """

    # Dependency
    START_EDGE_PROPERTIES = r"(?:\^\[)"
    END_EDGE_PROPERTIES = r"(?:\])"
    DEPENDENCY = r"(?:\^)"
    # Version
    VERSION_HASH_PAIR = rf"(?:@(?:{GIT_VERSION_PATTERN})=(?:{VERSION}))"
    GIT_VERSION = rf"@(?:{GIT_VERSION_PATTERN})"
    VERSION = rf"(?:@\s*(?:{VERSION_LIST}))"
    # Variants
    PROPAGATED_BOOL_VARIANT = rf"(?:(?:\+\+|~~|--)\s*{NAME})"
    BOOL_VARIANT = rf"(?:[~+-]\s*{NAME})"
    PROPAGATED_KEY_VALUE_PAIR = rf"(?:{NAME}==(?:{VALUE}|{QUOTED_VALUE}))"
    KEY_VALUE_PAIR = rf"(?:{NAME}=(?:{VALUE}|{QUOTED_VALUE}))"
    # Compilers
    COMPILER_AND_VERSION = rf"(?:%\s*(?:{NAME})(?:[\s]*)@\s*(?:{VERSION_LIST}))"
    COMPILER = rf"(?:%\s*(?:{NAME}))"
    # FILENAME
    FILENAME = rf"(?:{FILENAME})"
    # Package name
    FULLY_QUALIFIED_PACKAGE_NAME = rf"(?:{DOTTED_IDENTIFIER})"
    UNQUALIFIED_PACKAGE_NAME = rf"(?:{IDENTIFIER})"
    # DAG hash
    DAG_HASH = rf"(?:/(?:{HASH}))"
    # White spaces
    WS = r"(?:\s+)"


class ErrorTokenType(TokenBase):
    """Enum with regexes for error analysis"""

    # Unexpected character
    UNEXPECTED = r"(?:.[\s]*)"


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


#: List of all the regexes used to match spec parts, in order of precedence
TOKEN_REGEXES = [rf"(?P<{token}>{token.regex})" for token in TokenType]
#: List of all valid regexes followed by error analysis regexes
ERROR_HANDLING_REGEXES = TOKEN_REGEXES + [
    rf"(?P<{token}>{token.regex})" for token in ErrorTokenType
]
#: Regex to scan a valid text
ALL_TOKENS = re.compile("|".join(TOKEN_REGEXES))
#: Regex to analyze an invalid text
ANALYSIS_REGEX = re.compile("|".join(ERROR_HANDLING_REGEXES))


def tokenize(text: str) -> Iterator[Token]:
    """Return a token generator from the text passed as input.

    Raises:
        SpecTokenizationError: if we can't tokenize anymore, but didn't reach the
            end of the input text.
    """
    scanner = ALL_TOKENS.scanner(text)  # type: ignore[attr-defined]
    match: Optional[Match] = None
    for match in iter(scanner.match, None):
        # The following two assertions are to help mypy
        msg = (
            "unexpected value encountered during parsing. Please submit a bug report "
            "at https://github.com/spack/spack/issues/new/choose"
        )
        assert match is not None, msg
        assert match.lastgroup is not None, msg
        yield Token(
            TokenType.__members__[match.lastgroup], match.group(), match.start(), match.end()
        )

    if match is None and not text:
        # We just got an empty string
        return

    if match is None or match.end() != len(text):
        scanner = ANALYSIS_REGEX.scanner(text)  # type: ignore[attr-defined]
        matches = [m for m in iter(scanner.match, None)]  # type: ignore[var-annotated]
        raise SpecTokenizationError(matches, text)


class TokenContext:
    """Token context passed around by parsers"""

    __slots__ = "token_stream", "current_token", "next_token"

    def __init__(self, token_stream: Iterator[Token]):
        self.token_stream = token_stream
        self.current_token = None
        self.next_token = None
        self.advance()

    def advance(self):
        """Advance one token"""
        self.current_token, self.next_token = self.next_token, next(self.token_stream, None)

    def accept(self, kind: TokenType):
        """If the next token is of the specified kind, advance the stream and return True.
        Otherwise return False.
        """
        if self.next_token and self.next_token.kind == kind:
            self.advance()
            return True
        return False

    def expect(self, *kinds: TokenType):
        return self.next_token and self.next_token.kind in kinds


class SpecTokenizationError(SpecSyntaxError):
    """Syntax error in a spec string"""

    def __init__(self, matches, text):
        message = "unexpected tokens in the spec string\n"
        message += f"{text}"

        underline = "\n"
        for match in matches:
            if match.lastgroup == str(ErrorTokenType.UNEXPECTED):
                underline += f"{'^' * (match.end() - match.start())}"
                continue
            underline += f"{' ' * (match.end() - match.start())}"

        message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)
