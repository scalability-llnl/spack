# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import sys

from ctest_log_parser import BuildError, BuildWarning, CTestLogParser

import llnl.util.tty as tty
from llnl.util.tty.color import cescape, colorize

__all__ = ["parse_log_events", "make_log_context"]


def parse_log_events(stream, context=6, jobs=None, profile=False):
    """Extract interesting events from a log file as a list of LogEvent.

    Args:
        stream (str or typing.IO): build log name or file object
        context (int): lines of context to extract around each log event
        jobs (int): number of jobs to parse with; default ncpus
        profile (bool): print out profile information for parsing

    Returns:
        (tuple): two lists containig ``BuildError`` and
            ``BuildWarning`` objects.

    This is a wrapper around ``ctest_log_parser.CTestLogParser`` that
    lazily constructs a single ``CTestLogParser`` object.  This ensures
    that all the regex compilation is only done once.
    """
    if parse_log_events.ctest_parser is None:
        parse_log_events.ctest_parser = CTestLogParser(profile=profile)

    result = parse_log_events.ctest_parser.parse(stream, context, jobs)
    if profile:
        parse_log_events.ctest_parser.print_timings()
    return result


#: lazily constructed CTest log parser
parse_log_events.ctest_parser = None  # type: ignore[attr-defined]


def _wrap(text, width):
    """Break text into lines of specific width."""
    lines = []
    pos = 0
    while pos < len(text):
        lines.append(text[pos : pos + width])
        pos += width
    return lines


def make_log_context(log_events, width=None):
    """Get error context from a log file.

    Args:
        log_events (list): list of events created by
            ``ctest_log_parser.parse()``
        width (int or None): wrap width; ``0`` for no limit; ``None`` to
            auto-size for terminal
    Returns:
        str: context from the build log with errors highlighted

    Parses the log file for lines containing errors, and prints them out
    with line numbers and context.  Errors are highlighted with '>>' and
    with red highlighting (if color is enabled).

    Events are sorted by line number before they are displayed.
    """
    error_lines = set(e.line_no for e in log_events)
    log_events = sorted(log_events, key=lambda e: e.line_no)

    num_width = len(str(max(error_lines or [0]))) + 4
    line_fmt = "%%-%dd%%s" % num_width
    indent = " " * (5 + num_width)

    if width is None:
        _, width = tty.terminal_size()
    if width <= 0:
        width = sys.maxsize
    wrap_width = width - num_width - 6

    out = io.StringIO()
    next_line = 1
    for event in log_events:
        start = event.start

        if isinstance(event, BuildError):
            color = "R"
        elif isinstance(event, BuildWarning):
            color = "Y"
        else:
            color = "W"

        if next_line != 1 and start > next_line:
            out.write("\n     ...\n\n")

        if start < next_line:
            start = next_line

        for i in range(start, event.end):
            # wrap to width
            lines = _wrap(event[i], wrap_width)
            lines[1:] = [indent + ln for ln in lines[1:]]
            wrapped_line = line_fmt % (i, "\n".join(lines))

            if i in error_lines:
                out.write(colorize("  @%s{>> %s}\n" % (color, cescape(wrapped_line))))
            else:
                out.write("     %s\n" % wrapped_line)

        next_line = event.end

    return out.getvalue()
