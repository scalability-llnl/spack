# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import enum
import os
import re
from collections import defaultdict
from typing import Dict

import llnl.util.tty as tty

import spack.paths

description = "list and check license headers on files in spack"
section = "developer"
level = "long"

#: SPDX license id must appear in the first <license_lines> lines of a file
license_lines = 6

#: Spack's license identifier
apache2_mit_spdx = "(Apache-2.0 OR MIT)"

#: regular expressions for licensed files.
licensed_files = [
    # spack scripts
    r"^bin/spack$",
    r"^bin/spack\.bat$",
    r"^bin/spack\.ps1$",
    r"^bin/spack_pwsh\.ps1$",
    r"^bin/sbang$",
    r"^bin/spack-python$",
    r"^bin/haspywin\.py$",
    # all of spack core except unparse
    r"^lib/spack/spack_installable/main\.py$",
    r"^lib/spack/spack/(?!(test/)?util/unparse).*\.py$",
    r"^lib/spack/spack/.*\.sh$",
    r"^lib/spack/spack/.*\.lp$",
    r"^lib/spack/llnl/.*\.py$",
    r"^lib/spack/env/cc$",
    # special case some test data files that have license headers
    r"^lib/spack/spack/test/data/style/broken.dummy",
    r"^lib/spack/spack/test/data/unparse/.*\.txt",
    # rst files in documentation
    r"^lib/spack/docs/(?!command_index|spack|llnl).*\.rst$",
    r"^lib/spack/docs/.*\.py$",
    r"^lib/spack/docs/spack.yaml$",
    # 1 file in external
    r"^lib/spack/external/__init__.py$",
    # shell scripts in share
    r"^share/spack/.*\.sh$",
    r"^share/spack/.*\.bash$",
    r"^share/spack/.*\.csh$",
    r"^share/spack/.*\.fish$",
    r"^share/spack/setup-env\.ps1$",
    r"^share/spack/qa/run-[^/]*$",
    r"^share/spack/qa/*.py$",
    r"^share/spack/bash/spack-completion.in$",
    # action workflows
    r"^.github/actions/.*\.py$",
    # all packages
    r"^var/spack/repos/.*/package.py$",
]


def _all_spack_files(root=spack.paths.prefix):
    """Generates root-relative paths of all files in the spack repository."""
    visited = set()
    for cur_root, folders, files in os.walk(root):
        for filename in files:
            path = os.path.realpath(os.path.join(cur_root, filename))

            if path not in visited:
                yield os.path.relpath(path, root)
                visited.add(path)


def _licensed_files(args):
    for relpath in _all_spack_files(args.root):
        if any(regex.match(relpath) for regex in licensed_files):
            yield relpath


def list_files(args):
    """list files in spack that should have license headers"""
    for relpath in sorted(_licensed_files(args)):
        print(os.path.join(spack.paths.spack_root, relpath))


# Error codes for license verification. All values are chosen such that
# bool(value) evaluates to True
class ErrorType(enum.Enum):
    SPDX_MISMATCH = 1
    NOT_IN_FIRST_N_LINES = 2
    GENERAL_MISMATCH = 3


#: regexes for valid license lines at tops of files
license_line_regexes = [
    r"Copyright (Spack|sbang) [Pp]roject [Dd]evelopers\. See COPYRIGHT file for details.",
    r"",
    r"SPDX-License-Identifier: \(Apache-2\.0 OR MIT\)",
]


class LicenseError:
    error_counts: Dict[ErrorType, int]

    def __init__(self):
        self.error_counts = defaultdict(int)

    def add_error(self, error):
        self.error_counts[error] += 1

    def has_errors(self):
        return sum(self.error_counts.values()) > 0

    def error_messages(self):
        total = sum(self.error_counts.values())
        missing = self.error_counts[ErrorType.GENERAL_MISMATCH]
        lines = self.error_counts[ErrorType.NOT_IN_FIRST_N_LINES]
        spdx_mismatch = self.error_counts[ErrorType.SPDX_MISMATCH]
        return (
            f"{total} improperly licensed files",
            f"files with wrong SPDX-License-Identifier:   {spdx_mismatch}",
            f"files without license in first {license_lines} lines:     {lines}",
            f"files not containing expected license:      {missing}",
        )


def _check_license(lines, path):
    def sanitize(line):
        return re.sub(r"^[\s#\%\.\:]*", "", line).rstrip()

    for i, line in enumerate(lines):
        if all(
            re.match(regex, sanitize(lines[i + j])) for j, regex in enumerate(license_line_regexes)
        ):
            return

        if i >= (license_lines - len(license_line_regexes)):
            print(f"{path}: License not found in first {license_lines} lines")
            return ErrorType.NOT_IN_FIRST_N_LINES

    # If the SPDX identifier is present, then there is a mismatch (since it
    # did not match the above regex)
    def wrong_spdx_identifier(line, path):
        m = re.search(r"SPDX-License-Identifier: ([^\n]*)", line)
        if m and m.group(1) != apache2_mit_spdx:
            print(
                f"{path}: SPDX license identifier mismatch "
                f"(expecting {apache2_mit_spdx}, found {m.group(1)})"
            )
            return ErrorType.SPDX_MISMATCH

    checks = [wrong_spdx_identifier]

    for line in lines:
        for check in checks:
            error = check(line, path)
            if error:
                return error

    print(f"{path}: the license header at the top of the file does not match the expected format")
    return ErrorType.GENERAL_MISMATCH


def verify(args):
    """verify that files in spack have the right license header"""

    license_errors = LicenseError()

    for relpath in _licensed_files(args):
        path = os.path.join(args.root, relpath)
        with open(path, encoding="utf-8") as f:
            lines = [line for line in f][:license_lines]

        error = _check_license(lines, path)
        if error:
            license_errors.add_error(error)

    if license_errors.has_errors():
        tty.die(*license_errors.error_messages())
    else:
        tty.msg("No license issues found.")


def setup_parser(subparser):
    subparser.add_argument(
        "--root",
        action="store",
        default=spack.paths.prefix,
        help="scan a different prefix for license issues",
    )

    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="license_command")
    sp.add_parser("list-files", help=list_files.__doc__)
    sp.add_parser("verify", help=verify.__doc__)


def license(parser, args):
    licensed_files[:] = [re.compile(regex) for regex in licensed_files]

    commands = {"list-files": list_files, "verify": verify}
    return commands[args.license_command](args)
