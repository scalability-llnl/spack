# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file implements an expression syntax, similar to ``printf``, for adding
ANSI colors to text.

See ``colorize()``, ``cwrite()``, and ``cprint()`` for routines that can
generate colored output.

``colorize`` will take a string and replace all color expressions with
ANSI control codes.  If the ``isatty`` keyword arg is set to False, then
the color expressions will be converted to null strings, and the
returned string will have no color.

``cwrite`` and ``cprint`` are equivalent to ``write()`` and ``print()``
calls in python, but they colorize their output.  If the ``stream`` argument is
not supplied, they write to ``sys.stdout``.

Here are some example color expressions:

==========  ============================================================
Expression  Meaning
==========  ============================================================
@r          Turn on red coloring
@-r         Turn on red coloring, and strike through text
@R          Turn on bright red coloring
@*{foo}     Bold foo, but don't change text color
@_{bar}     Underline bar, but don't change text color
@*b         Turn on bold, blue text
@_B         Turn on bright blue text with an underline
@.          Revert to plain formatting
@*g{green}  Print out 'green' in bold, green text, then reset to plain.
@*ggreen@.  Print out 'green' in bold, green text, then reset to plain.
==========  ============================================================

The syntax consists of:

==========  =================================================
color-expr  '@' [style] color-code '{' text '}' | '@.' | '@@'
style       '*' | '_'
color-code  [krgybmcwKRGYBMCW]
text        .*
==========  =================================================

'@' indicates the start of a color expression.  It can be followed
by an optional * or _ that indicates whether the font should be bold or
underlined.  If * or _ is not provided, the text will be plain.  Then
an optional color code is supplied.  This can be [krgybmcw] or [KRGYBMCW],
where the letters map to  black(k), red(r), green(g), yellow(y), blue(b),
magenta(m), cyan(c), and white(w).  Lowercase letters denote normal ANSI
colors and capital letters denote bright ANSI colors.

Finally, the color expression can be followed by text enclosed in {}.  If
braces are present, only the text in braces is colored.  If the braces are
NOT present, then just the control codes to enable the color will be output.
The console can be reset later to plain text with '@.'.

To output an @, use '@@'.  To output a } inside braces, use '}}'.
"""
from __future__ import unicode_literals
import re
import sys

from contextlib import contextmanager

import six


class ColorParseError(Exception):
    """Raised when a color format fails to parse."""

    def __init__(self, message):
        super(ColorParseError, self).__init__(message)


# Text styles for ansi codes
styles = {'*': '1',       # bold
          '_': '4',       # underline
          '-': '9',       # strikethrough
          None: '0'}      # plain

# Dim and bright ansi colors
colors = {'k': 30, 'K': 90,  # black
          'r': 31, 'R': 91,  # red
          'g': 32, 'G': 92,  # green
          'y': 33, 'Y': 93,  # yellow
          'b': 34, 'B': 94,  # blue
          'm': 35, 'M': 95,  # magenta
          'c': 36, 'C': 96,  # cyan
          'w': 37, 'W': 97}  # white

# Regex to be used for color formatting
color_re = r'@(?:@|\.|([*_-])?([a-zA-Z])?(?:{((?:[^}]|}})*)})?)'

# Mapping from color arguments to values for tty.set_color
color_when_values = {
    'always': True,
    'auto': None,
    'never': False
}

# Force color; None: Only color if stdout is a tty
# True: Always colorize output, False: Never colorize output
_force_color = None


def _color_when_value(when):
    """Raise a ValueError for an invalid color setting.

    Valid values are 'always', 'never', and 'auto', or equivalently,
    True, False, and None.
    """
    if when in color_when_values:
        return color_when_values[when]
    elif when not in color_when_values.values():
        raise ValueError('Invalid color setting: %s' % when)
    return when


def get_color_when():
    """Return whether commands should print color or not."""
    if _force_color is not None:
        return _force_color
    return sys.stdout.isatty()


def set_color_when(when):
    """Set when color should be applied.  Options are:

    * True or 'always': always print color
    * False or 'never': never print color
    * None or 'auto': only print color if sys.stdout is a tty.
    """
    global _force_color
    _force_color = _color_when_value(when)


@contextmanager
def color_when(value):
    """Context manager to temporarily use a particular color setting."""
    old_value = value
    set_color_when(value)
    yield
    set_color_when(old_value)


class match_to_ansi(object):

    def __init__(self, color=True):
        self.color = _color_when_value(color)

    def escape(self, s):
        """Returns a TTY escape sequence for a color"""
        if self.color:
            return "\033[%sm" % s
        else:
            return ''

    def __call__(self, match):
        """Convert a match object generated by ``color_re`` into an ansi
        color code. This can be used as a handler in ``re.sub``.
        """
        style, color, text = match.groups()
        m = match.group(0)

        if m == '@@':
            return '@'
        elif m == '@.':
            return self.escape(0)
        elif m == '@':
            raise ColorParseError("Incomplete color format: '%s' in %s"
                                  % (m, match.string))

        string = styles[style]
        if color:
            if color not in colors:
                raise ColorParseError("Invalid color specifier: '%s' in '%s'"
                                      % (color, match.string))
            string += ';' + str(colors[color])

        colored_text = ''
        if text:
            colored_text = text + self.escape(0)

        return self.escape(string) + colored_text


def colorize(string, **kwargs):
    """Replace all color expressions in a string with ANSI control codes.

    Args:
        string (str): The string to replace

    Returns:
        str: The filtered string

    Keyword Arguments:
        color (bool): If False, output will be plain text without control
            codes, for output to non-console devices.
    """
    color = _color_when_value(kwargs.get('color', get_color_when()))
    string = re.sub(color_re, match_to_ansi(color), string)
    string = string.replace('}}', '}')
    return string


def clen(string):
    """Return the length of a string, excluding ansi color sequences."""
    return len(re.sub(r'\033[^m]*m', '', string))


def cextra(string):
    """Length of extra color characters in a string"""
    return len(''.join(re.findall(r'\033[^m]*m', string)))


def cwrite(string, stream=None, color=None):
    """Replace all color expressions in string with ANSI control
       codes and write the result to the stream.  If color is
       False, this will write plain text with no color.  If True,
       then it will always write colored output.  If not supplied,
       then it will be set based on stream.isatty().
    """
    stream = sys.stdout if stream is None else stream
    if color is None:
        color = get_color_when()
    stream.write(colorize(string, color=color))


def cprint(string, stream=None, color=None):
    """Same as cwrite, but writes a trailing newline to the stream."""
    stream = sys.stdout if stream is None else stream
    cwrite(string + "\n", stream, color)


def cescape(string):
    """Escapes special characters needed for color codes.

    Replaces the following symbols with their equivalent literal forms:

    =====  ======
    ``@``  ``@@``
    ``}``  ``}}``
    =====  ======

    Parameters:
        string (str): the string to escape

    Returns:
        (str): the string with color codes escaped
    """
    string = six.text_type(string)
    string = string.replace('@', '@@')
    string = string.replace('}', '}}')
    return string


class ColorStream(object):

    def __init__(self, stream, color=None):
        self._stream = stream
        self._color = color

    def write(self, string, **kwargs):
        raw = kwargs.get('raw', False)
        raw_write = getattr(self._stream, 'write')

        color = self._color
        if self._color is None:
            if raw:
                color = True
            else:
                color = get_color_when()
        raw_write(colorize(string, color=color))

    def writelines(self, sequence, **kwargs):
        raw = kwargs.get('raw', False)
        for string in sequence:
            self.write(string, self.color, raw=raw)
