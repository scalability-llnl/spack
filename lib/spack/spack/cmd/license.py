# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import enum
import os
import re
import shutil
import tempfile
from typing import List, Optional, Tuple

import llnl.util.tty as tty

import spack.paths

description = "list and check license headers on files in spack"
section = "developer"
level = "long"

#: SPDX license id must appear in the first <license_lines> lines of a file
license_lines = 7

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
    r"^lib/spack/spack/.*-test-script$",  # for testing
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

#: lines for `spack license fix`
fixed_lines = [
    "# Copyright Spack Project Developers. See COPYRIGHT file for details.",
    "#",
    "# SPDX-License-Identifier: (Apache-2.0 OR MIT)",
]


class LicenseError:
    errors: List[Tuple[ErrorType, str]]

    def __init__(self):
        self.errors = []

    def add_error(self, error: ErrorType, path: str) -> None:
        self.errors.append((error, path))

    def has_errors(self) -> bool:
        return bool(self.errors)

    def print_and_die(self) -> None:
        spdx_mismatch = missing = first_n_lines = 0
        for err, path in self.errors:
            if err == ErrorType.SPDX_MISMATCH:
                print(f"{path}: SPDX license identifier mismatch (expected {apache2_mit_spdx})")
                spdx_mismatch += 1
            elif err == ErrorType.GENERAL_MISMATCH:
                print(f"{path}: license header at top of file does not match expected format")
                missing += 1
            elif err == ErrorType.NOT_IN_FIRST_N_LINES:
                print(f"{path}: License not found in first {license_lines} lines")
                first_n_lines += 1

        tty.die(
            f"{len(self.errors)} improperly licensed files",
            f"files with wrong SPDX-License-Identifier:   {spdx_mismatch}",
            f"files without license in first {license_lines} lines:     {first_n_lines}",
            f"files not containing expected license:      {missing}",
            "",
            "Try running `spack license fix` to fix these files.",
        )


def _check_license(lines: List[str], path: str) -> Optional[ErrorType]:
    sanitized = [re.sub(r"^[\s#\%\.\:]*", "", line).rstrip() for line in lines]

    # if start and end of license are not somewhere in the first n lines, say we didn't
    # see a license header at all.
    if not (
        any(line.startswith("Copyright") for line in sanitized)
        and any(line.startswith("SPDX") for line in sanitized)
    ):
        return ErrorType.NOT_IN_FIRST_N_LINES

    # compare sliding window of sanitized lines with license regexes -- correct case
    for i in range(len(sanitized) - len(license_line_regexes) + 1):
        if all(re.match(regex, sanitized[i + j]) for j, regex in enumerate(license_line_regexes)):
            return None

    # If the SPDX identifier is present, then report that specifically
    for line in lines:
        m = re.search(r"SPDX-License-Identifier: ([^\n]*)", line)
        if m and m.group(1) != apache2_mit_spdx:
            return ErrorType.SPDX_MISMATCH

    # if there's some other format issue, say the license doesn't look familiar.
    return ErrorType.GENERAL_MISMATCH


def _find_license_errors(args) -> LicenseError:
    """Find all license errors and return a LicenseError object."""
    license_errors = LicenseError()

    for relpath in _licensed_files(args):
        path = os.path.join(args.root, relpath)
        with open(path, encoding="utf-8") as f:
            lines = [line for line in f][:license_lines]

        error = _check_license(lines, path)
        if error:
            license_errors.add_error(error, path)

    return license_errors


def verify(args):
    """verify that files in spack have the right license header"""
    license_errors = _find_license_errors(args)
    if license_errors.has_errors():
        license_errors.print_and_die()
    else:
        tty.msg("No license issues found.")


def _fix_path(path: str) -> List[str]:
    """Fix the license of a spack file using some simple heuristics.

    This runs `spack license verify` and fixes the bad files (if it can).

    1. If there already appears to alrady be a familiar-looking license header,
       replace that license header with the canonical one.
    2. If there is no license header in a file, attempt to add one, taking into account
       shebangs for scripts.

    Returns:
        List of fixed lines, if a fix was possible, otherwise an empty list.
    """
    lines = open(path, encoding="utf-8").read().split("\n")

    # only try to fix python files / scripts
    if not (path.endswith(".py") or path.endswith(".sh") or (lines and lines[0].startswith("#!"))):
        return []

    # easy case: license looks mostly familiar
    start = next((i for i, line in enumerate(lines) if re.match(r"#\s*Copyright", line)), -1)
    end = next((i for i, line in enumerate(lines) if re.match(r"#\s*SPDX-", line)), -1)

    # here we just replace a bad license with the fixed one
    if start >= 0 and end >= 0:
        # filter out weird cases and make sure we mostly know what we're fixing
        if (
            end < start
            or end - start > 6
            or not all(lines[i].startswith("#") for i in range(start, end))
        ):
            return []

        if start < (license_lines - len(license_line_regexes)):
            # replace license where it is
            lines[start : end + 1] = fixed_lines
        else:
            # move license to beginning of file
            del lines[start : end + 1]

            start = 0
            while any(lines[start].startswith(s) for s in ("#!", "# -*-")):
                start += 1

            lines[start:start] = fixed_lines

        return lines

    # no license in the file yet, so we add it
    if start == -1 and end == -1:
        start = 0
        while any(lines[start].startswith(s) for s in ("#!", "# -*-")):
            start += 1

            # add an empty line if needed
            if not re.match(r"#\s*$", lines[start]):
                lines[start:start] = "#"
                start += 1

        lines[start:start] = fixed_lines
        return lines

    return []


def fix(args):
    """Fix files without proper licenses."""
    license_errors = _find_license_errors(args)
    if not license_errors.has_errors():
        tty.msg("No license issues found.")
        return

    returncode = 0
    for error_type, path in license_errors.errors:
        lines = _fix_path(path)
        if not lines:
            print(f"I don't know how to fix {path}")
            returncode = 1
            continue

        parent = os.path.dirname(path)
        with tempfile.NamedTemporaryFile("w", dir=parent, delete=False) as temp:
            temp.write("\n".join(lines))
        shutil.copymode(path, temp.name)
        os.rename(temp.name, path)
        print(f"Fixed {path}")

    return returncode


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
    sp.add_parser("fix", help=fix.__doc__)


def license(parser, args):
    licensed_files[:] = [re.compile(regex) for regex in licensed_files]

    commands = {"list-files": list_files, "verify": verify, "fix": fix}
    return commands[args.license_command](args)
