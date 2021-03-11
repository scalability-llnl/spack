# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import shlex
import sys
import itertools
from textwrap import dedent
from six import string_types

import spack.error


class Token(object):
    """Represents tokens; generated from input by lexer and fed to parse()."""

    def __init__(self, type, value='', start=0, end=0):
        self.type = type
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<%d: '%s'>" % (self.type, self.value)

    def is_a(self, type):
        return self.type == type

    def __eq__(self, other):
        return (self.type == other.type) and (self.value == other.value)


class Lexer(object):
    """Base class for Lexers that keep track of line numbers."""

    def __init__(self, lexicon_and_mode_switches):
        self.scanners = []
        self.switchbook = []
        for lexicon, mode_switches_dict in lexicon_and_mode_switches:
            self.scanners.append(re.Scanner(lexicon))
            self.switchbook.append(mode_switches_dict)

        self.mode = 0

    def token(self, type, value=''):
        cur_scanner = self.scanners[self.mode]
        return Token(type, value,
                     cur_scanner.match.start(0),
                     cur_scanner.match.end(0))

    def lex_word(self, word):
        scanner = self.scanners[self.mode]
        mode_switches_dict = self.switchbook[self.mode]

        tokens, remainder = scanner.scan(word)
        remainder_was_used = False

        for i, t in enumerate(tokens):
            for other_mode, mode_switches in mode_switches_dict.items():
                if t.type in mode_switches:
                    # Combine post-switch tokens with remainder and
                    # scan in other mode
                    self.mode = other_mode  # swap 0/1
                    remainder_was_used = True
                    tokens = tokens[:i + 1] + self.lex_word(
                        word[word.index(t.value) + len(t.value):])
                    break

        if remainder and not remainder_was_used:
            raise LexError("Invalid character", word, word.index(remainder))

        return tokens

    def lex(self, text):
        lexed = []
        for word in text:
            tokens = self.lex_word(word)
            lexed.extend(tokens)
        return lexed


class Parser(object):
    """Base class for simple recursive descent parsers."""

    def __init__(self, lexer):
        self.tokens = iter([])    # iterators over tokens, handled in order.
        self.token = Token(None)  # last accepted token
        self.next = None          # next token
        self.lexer = lexer
        self.text = None

    def gettok(self):
        """Puts the next token in the input stream into self.next."""
        try:
            self.next = next(self.tokens)
        except StopIteration:
            self.next = None

    def push_tokens(self, iterable):
        """Adds all tokens in some iterable to the token stream."""
        self.tokens = itertools.chain(
            iter(iterable), iter([self.next]), self.tokens)
        self.gettok()

    def accept(self, id):
        """Put the next symbol in self.token if accepted, then call gettok()"""
        if self.next and self.next.is_a(id):
            self.token = self.next
            self.gettok()
            return True
        return False

    def next_token_error(self, message):
        """Raise an error about the next token in the stream."""
        raise ParseError(message, self.text, self.token.end)

    def last_token_error(self, message):
        """Raise an error about the previous token in the stream."""
        raise ParseError(message, self.text, self.token.start)

    def unexpected_token(self):
        self.next_token_error("Unexpected token: '%s'" % self.next.value)

    def expect(self, id):
        """Like accept(), but fails if we don't like the next token."""
        if self.accept(id):
            return True
        else:
            if self.next:
                self.unexpected_token()
            else:
                self.next_token_error("Unexpected end of input")
            sys.exit(1)

    def setup(self, text):
        if isinstance(text, string_types):
            text = shlex.split(str(text))
        self.text = text
        self.push_tokens(self.lexer.lex(text))

    def parse(self, text):
        self.setup(text)
        return self.do_parse()


class ParseError(spack.error.SpackError):
    """Raised when we hit an error while parsing."""

    def __init__(self, message, string, pos):
        super(ParseError, self).__init__(message)
        self.string = string
        self.pos = pos


class LexError(ParseError):
    """Raised when we don't know how to lex something."""

    def __init__(self, message, string, pos):
        bad_char = string[pos]
        printed = dedent("""\
        {0}: '{1}'
        -------
        {2}
        {3}^
        """).format(message, bad_char, string, pos * ' ')
        super(LexError, self).__init__(printed, string, pos)
