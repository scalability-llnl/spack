# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import io
import os
import struct
import sys
import textwrap
import traceback
from datetime import datetime
from sys import platform as _platform
from typing import Any, NoReturn

if _platform != "win32":
    import fcntl
    import termios

from llnl.util.tty.color import cescape, clen, cprint, cwrite

# Globals
_debug = 0
_verbose = False
_stacktrace = False
_timestamp = False
_msg_enabled = True
_warn_enabled = True
_error_enabled = True
_output_filter = lambda s: s
indent = "  "


def debug_level():
    return _debug


def is_verbose():
    return _verbose


def is_debug(level=1):
    return _debug >= level


def set_debug(level=0):
    global _debug
    assert level >= 0, "Debug level must be a positive value"
    _debug = level


def set_verbose(flag):
    global _verbose
    _verbose = flag


def set_timestamp(flag):
    global _timestamp
    _timestamp = flag


def set_msg_enabled(flag):
    global _msg_enabled
    _msg_enabled = flag


def set_warn_enabled(flag):
    global _warn_enabled
    _warn_enabled = flag


def set_error_enabled(flag):
    global _error_enabled
    _error_enabled = flag


def msg_enabled():
    return _msg_enabled


def warn_enabled():
    return _warn_enabled


def error_enabled():
    return _error_enabled


@contextlib.contextmanager
def output_filter(filter_fn):
    """Context manager that applies a filter to all output."""
    global _output_filter
    saved_filter = _output_filter
    try:
        _output_filter = filter_fn
        yield
    finally:
        _output_filter = saved_filter


class SuppressOutput:
    """Class for disabling output in a scope using 'with' keyword"""

    def __init__(self, msg_enabled=True, warn_enabled=True, error_enabled=True):
        self._msg_enabled_initial = _msg_enabled
        self._warn_enabled_initial = _warn_enabled
        self._error_enabled_initial = _error_enabled

        self._msg_enabled = msg_enabled
        self._warn_enabled = warn_enabled
        self._error_enabled = error_enabled

    def __enter__(self):
        set_msg_enabled(self._msg_enabled)
        set_warn_enabled(self._warn_enabled)
        set_error_enabled(self._error_enabled)

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_msg_enabled(self._msg_enabled_initial)
        set_warn_enabled(self._warn_enabled_initial)
        set_error_enabled(self._error_enabled_initial)


def set_stacktrace(flag):
    global _stacktrace
    _stacktrace = flag


def process_stacktrace(countback):
    """Gives file and line frame 'countback' frames from the bottom"""
    st = traceback.extract_stack()
    # Not all entries may be spack files, we have to remove those that aren't.
    file_list = []
    for frame in st:
        # Check that the file is a spack file
        if frame[0].find(os.path.sep + "spack") >= 0:
            file_list.append(frame[0])
    # We use commonprefix to find what the spack 'root' directory is.
    root_dir = os.path.commonprefix(file_list)
    root_len = len(root_dir)
    st_idx = len(st) - countback - 1
    st_text = "%s:%i " % (st[st_idx][0][root_len:], st[st_idx][1])
    return st_text


def show_pid():
    return is_debug(2)


def get_timestamp(force=False):
    """Get a string timestamp"""
    if _debug or _timestamp or force:
        # Note inclusion of the PID is useful for parallel builds.
        pid = ", {0}".format(os.getpid()) if show_pid() else ""
        return "[{0}{1}] ".format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"), pid)
    else:
        return ""


def msg(message: Any, *args: Any, newline: bool = True) -> None:
    if not msg_enabled():
        return

    if isinstance(message, Exception):
        message = f"{message.__class__.__name__}: {message}"
    else:
        message = str(message)

    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(2)

    nl = "\n" if newline else ""
    cwrite(f"@*b{{{st_text}==>}} {get_timestamp()}{cescape(_output_filter(message))}{nl}")

    for arg in args:
        print(indent + _output_filter(str(arg)))


def info(message, *args, **kwargs):
    if isinstance(message, Exception):
        message = "%s: %s" % (message.__class__.__name__, str(message))

    format = kwargs.get("format", "*b")
    stream = kwargs.get("stream", sys.stdout)
    wrap = kwargs.get("wrap", False)
    break_long_words = kwargs.get("break_long_words", False)
    st_countback = kwargs.get("countback", 3)

    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(st_countback)
    cprint(
        "@%s{%s==>} %s%s"
        % (format, st_text, get_timestamp(), cescape(_output_filter(str(message)))),
        stream=stream,
    )
    for arg in args:
        if wrap:
            lines = textwrap.wrap(
                _output_filter(str(arg)),
                initial_indent=indent,
                subsequent_indent=indent,
                break_long_words=break_long_words,
            )
            for line in lines:
                stream.write(line + "\n")
        else:
            stream.write(indent + _output_filter(str(arg)) + "\n")
    stream.flush()


def verbose(message, *args, **kwargs):
    if _verbose:
        kwargs.setdefault("format", "c")
        info(message, *args, **kwargs)


def debug(message, *args, **kwargs):
    level = kwargs.get("level", 1)
    if is_debug(level):
        kwargs.setdefault("format", "g")
        kwargs.setdefault("stream", sys.stderr)
        info(message, *args, **kwargs)


def error(message, *args, **kwargs):
    if not error_enabled():
        return

    kwargs.setdefault("format", "*r")
    kwargs.setdefault("stream", sys.stderr)
    info("Error: " + str(message), *args, **kwargs)


def warn(message, *args, **kwargs):
    if not warn_enabled():
        return

    kwargs.setdefault("format", "*Y")
    kwargs.setdefault("stream", sys.stderr)
    info("Warning: " + str(message), *args, **kwargs)


def die(message, *args, **kwargs) -> NoReturn:
    kwargs.setdefault("countback", 4)
    error(message, *args, **kwargs)
    sys.exit(1)


def get_yes_or_no(prompt, **kwargs):
    default_value = kwargs.get("default", None)

    if default_value is None:
        prompt += " [y/n] "
    elif default_value is True:
        prompt += " [Y/n] "
    elif default_value is False:
        prompt += " [y/N] "
    else:
        raise ValueError("default for get_yes_no() must be True, False, or None.")

    result = None
    while result is None:
        msg(prompt, newline=False)
        ans = input().lower()
        if not ans:
            result = default_value
            if result is None:
                print("Please enter yes or no.")
        else:
            if ans == "y" or ans == "yes":
                result = True
            elif ans == "n" or ans == "no":
                result = False
    return result


def hline(label=None, **kwargs):
    """Draw a labeled horizontal line.

    Keyword Arguments:
        char (str): Char to draw the line with.  Default '-'
        max_width (int): Maximum width of the line.  Default is 64 chars.
    """
    char = kwargs.pop("char", "-")
    max_width = kwargs.pop("max_width", 64)
    if kwargs:
        raise TypeError(
            "'%s' is an invalid keyword argument for this function." % next(kwargs.iterkeys())
        )

    rows, cols = terminal_size()
    if not cols:
        cols = max_width
    else:
        cols -= 2
    cols = min(max_width, cols)

    label = str(label)
    prefix = char * 2 + " "
    suffix = " " + (cols - len(prefix) - clen(label)) * char

    out = io.StringIO()
    out.write(prefix)
    out.write(label)
    out.write(suffix)

    print(out.getvalue())


def terminal_size():
    """Gets the dimensions of the console: (rows, cols)."""
    if _platform != "win32":

        def ioctl_gwinsz(fd):
            try:
                rc = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
            except BaseException:
                return
            return rc

        rc = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
        if not rc:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                rc = ioctl_gwinsz(fd)
                os.close(fd)
            except BaseException:
                pass
        if not rc:
            rc = (os.environ.get("LINES", 25), os.environ.get("COLUMNS", 80))

        return int(rc[0]), int(rc[1])
    else:
        rc = (os.environ.get("LINES", 25), os.environ.get("COLUMNS", 80))
        return int(rc[0]), int(rc[1])
