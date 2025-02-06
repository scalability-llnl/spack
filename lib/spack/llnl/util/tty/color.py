# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
import os
import re
import sys
from contextlib import contextmanager
from typing import Optional


class ColorParseError(Exception):
    """Raised when a color format fails to parse."""

    def __init__(self, message):
        super().__init__(message)


# Text styles for ansi codes
styles = {"*": "1", "_": "4", None: "0"}  # bold  # underline  # plain

# Dim and bright ansi colors
colors = {
    "k": 30,
    "K": 90,  # black
    "r": 31,
    "R": 91,  # red
    "g": 32,
    "G": 92,  # green
    "y": 33,
    "Y": 93,  # yellow
    "b": 34,
    "B": 94,  # blue
    "m": 35,
    "M": 95,  # magenta
    "c": 36,
    "C": 96,  # cyan
    "w": 37,
    "W": 97,
}  # white

# Regex to be used for color formatting
COLOR_RE = re.compile(r"@(?:(@)|(\.)|([*_])?([a-zA-Z])?(?:{((?:[^}]|}})*)})?)")

# Mapping from color arguments to values for tty.set_color
color_when_values = {"always": True, "auto": None, "never": False}


def _color_when_value(when):
    """Raise a ValueError for an invalid color setting.

    Valid values are 'always', 'never', and 'auto', or equivalently,
    True, False, and None.
    """
    if when in color_when_values:
        return color_when_values[when]
    elif when not in color_when_values.values():
        raise ValueError("Invalid color setting: %s" % when)
    return when


def _color_from_environ() -> Optional[bool]:
    try:
        return _color_when_value(os.environ.get("SPACK_COLOR", "auto"))
    except ValueError:
        return None


#: When `None` colorize when stdout is tty, when `True` or `False` always or never colorize resp.
_force_color = _color_from_environ()


def try_enable_terminal_color_on_windows():
    """Turns coloring in Windows terminal by enabling VTP in Windows consoles (CMD/PWSH/CONHOST)
    Method based on the link below
    https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences#example-of-enabling-virtual-terminal-processing

    Note: No-op on non windows platforms
    """
    if sys.platform == "win32":
        import ctypes
        import msvcrt
        from ctypes import wintypes

        try:
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            DISABLE_NEWLINE_AUTO_RETURN = 0x0008
            kernel32 = ctypes.WinDLL("kernel32")

            def _err_check(result, func, args):
                if not result:
                    raise ctypes.WinError(ctypes.get_last_error())
                return args

            kernel32.GetConsoleMode.errcheck = _err_check
            kernel32.GetConsoleMode.argtypes = (
                wintypes.HANDLE,  # hConsoleHandle, i.e. GetStdHandle output type
                ctypes.POINTER(wintypes.DWORD),  # result of GetConsoleHandle
            )
            kernel32.SetConsoleMode.errcheck = _err_check
            kernel32.SetConsoleMode.argtypes = (
                wintypes.HANDLE,  # hConsoleHandle, i.e. GetStdHandle output type
                wintypes.DWORD,  # result of GetConsoleHandle
            )
            # Use conout$ here to handle a redirectired stdout/get active console associated
            # with spack
            with open(r"\\.\CONOUT$", "w", encoding="utf-8") as conout:
                # Link above would use kernel32.GetStdHandle(-11) however this would not handle
                # a redirected stdout appropriately, so we always refer to the current CONSOLE out
                # which is defined as conout$ on Windows.
                # linked example is follow more or less to the letter beyond this point
                con_handle = msvcrt.get_osfhandle(conout.fileno())
                dw_orig_mode = wintypes.DWORD()
                kernel32.GetConsoleMode(con_handle, ctypes.byref(dw_orig_mode))
                dw_new_mode_request = (
                    ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN
                )
                dw_new_mode = dw_new_mode_request | dw_orig_mode.value
                kernel32.SetConsoleMode(con_handle, wintypes.DWORD(dw_new_mode))
        except OSError:
            # We failed to enable color support for associated console
            # report and move on but spack will no longer attempt to
            # color
            global _force_color
            _force_color = False
            from . import debug

            debug("Unable to support color on Windows terminal")


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


def _escape(s: str, color: bool, enclose: bool, zsh: bool) -> str:
    """Returns a TTY escape sequence for a color"""
    if color:
        if zsh:
            result = rf"\e[0;{s}m"
        else:
            result = f"\033[{s}m"

        if enclose:
            result = rf"\[{result}\]"

        return result
    else:
        return ""


def colorize(
    string: str, color: Optional[bool] = None, enclose: bool = False, zsh: bool = False
) -> str:
    """Replace all color expressions in a string with ANSI control codes.

    Args:
        string: The string to replace

    Returns:
        The filtered string

    Keyword Arguments:
        color: If False, output will be plain text without control codes, for output to
            non-console devices (default: automatically choose color or not)
        enclose: If True, enclose ansi color sequences with
            square brackets to prevent misestimation of terminal width.
        zsh: If True, use zsh ansi codes instead of bash ones (for variables like PS1)
    """
    color = color if color is not None else get_color_when()

    def match_to_ansi(match):
        """Convert a match object generated by ``COLOR_RE`` into an ansi
        color code. This can be used as a handler in ``re.sub``.
        """
        escaped_at, dot, style, color_code, text = match.groups()

        if escaped_at:
            return "@"
        elif dot:
            return _escape(0, color, enclose, zsh)
        elif not (style or color_code):
            raise ColorParseError(
                f"Incomplete color format: '{match.group(0)}' in '{match.string}'"
            )

        color_number = colors.get(color_code, "")
        semi = ";" if color_number else ""
        ansi_code = _escape(f"{styles[style]}{semi}{color_number}", color, enclose, zsh)
        if text:
            return f"{ansi_code}{text}{_escape(0, color, enclose, zsh)}"
        else:
            return ansi_code

    return COLOR_RE.sub(match_to_ansi, string).replace("}}", "}")


def clen(string):
    """Return the length of a string, excluding ansi color sequences."""
    return len(re.sub(r"\033[^m]*m", "", string))


def cextra(string):
    """Length of extra color characters in a string"""
    return len("".join(re.findall(r"\033[^m]*m", string)))


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


def cescape(string: str) -> str:
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
    return string.replace("@", "@@").replace("}", "}}")


class ColorStream:
    def __init__(self, stream, color=None):
        self._stream = stream
        self._color = color

    def write(self, string, **kwargs):
        raw = kwargs.get("raw", False)
        raw_write = getattr(self._stream, "write")

        color = self._color
        if self._color is None:
            if raw:
                color = True
            else:
                color = get_color_when()
        raw_write(colorize(string, color=color))

    def writelines(self, sequence, **kwargs):
        raw = kwargs.get("raw", False)
        for string in sequence:
            self.write(string, self.color, raw=raw)
