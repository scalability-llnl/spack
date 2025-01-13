# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
import sys
from collections import defaultdict

import pycodestyle
from flake8.formatting.default import Pylint
from flake8.style_guide import Violation

#: This is a dict that maps:
#:  filename pattern ->
#:     flake8 exemption code ->
#:        list of patterns, for which matching lines should have codes applied.
#:
#: For each file, if the filename pattern matches, we'll add per-line
#: exemptions if any patterns in the sub-dict match.
pattern_exemptions = {
    # exemptions applied only to package.py files.
    r"package.py$": {
        # Allow 'from spack.package import *' in packages, but no other wildcards
        "F403": [r"^from spack.package import \*$", r"^from spack.package_defs import \*$"],
        # Exempt '@when' decorated functions from redefinition errors.
        "F811": [r"^\s*@when\(.*\)"],
    },
    # exemptions applied to all files.
    r".py$": {
        "E501": [
            r"(ssh|https?|ftp|file)\:",  # URLs
            r'([\'"])[0-9a-fA-F]{32,}\1',  # long hex checksums
        ]
    },
}


# compile all regular expressions.
pattern_exemptions = dict(
    (
        re.compile(file_pattern),
        dict((code, [re.compile(p) for p in patterns]) for code, patterns in error_dict.items()),
    )
    for file_pattern, error_dict in pattern_exemptions.items()
)


class SpackFormatter(Pylint):
    def __init__(self, options):
        self.spack_errors = {}
        self.error_seen = False
        super().__init__(options)

    def after_init(self) -> None:
        """Overriding to keep format string from being unset in Default"""
        pass

    def beginning(self, filename):
        self.filename = filename
        self.file_lines = None
        self.spack_errors = defaultdict(list)
        for file_pattern, errors in pattern_exemptions.items():
            if file_pattern.search(filename):
                for code, pat_arr in errors.items():
                    self.spack_errors[code].extend(pat_arr)

    def handle(self, error: Violation) -> None:
        """Handle an error reported by Flake8.

        This defaults to calling :meth:`format`, :meth:`show_source`, and
        then :meth:`write`. This version implements the pattern-based ignore
        behavior from `spack flake8` as a native flake8 plugin.

        :param error:
            This will be an instance of
            :class:`~flake8.style_guide.Violation`.
        """

        # print(error.code)
        # print(error.physical_line)
        # get list of patterns for this error code
        pats = self.spack_errors.get(error.code, None)
        # if any pattern matches, skip line
        if pats is not None and any((pat.search(error.physical_line) for pat in pats)):
            return

        # Special F811 handling
        # Prior to Python 3.8, `noqa: F811` needed to be placed on the `@when`
        # line
        # Starting with Python 3.8, it must be placed on the `def` line
        # https://gitlab.com/pycqa/flake8/issues/583
        # we can only determine if F811 should be ignored given the previous
        # line, so get the previous line and check it
        if self.spack_errors.get("F811", False) and error.code == "F811" and error.line_number > 1:
            if self.file_lines is None:
                if self.filename in {"stdin", "-", "(none)", None}:
                    self.file_lines = pycodestyle.stdin_get_value().splitlines(True)
                else:
                    self.file_lines = pycodestyle.readlines(self.filename)
            for pat in self.spack_errors["F811"]:
                if pat.search(self.file_lines[error.line_number - 2]):
                    return

        self.error_seen = True
        line = self.format(error)
        source = self.show_source(error)
        self.write(line, source)

    def stop(self):
        """Override stop to check whether any errors we consider to be errors
        were reported.

        This is a hack, but it makes flake8 behave the desired way.
        """
        if not self.error_seen:
            sys.exit(0)
