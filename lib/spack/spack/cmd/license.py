# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime
import os
import pathlib
import re
from collections import defaultdict
from typing import List

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.paths

description = "list and check license headers on files in spack"
section = "developer"
level = "long"

#: SPDX license id must appear in the first <license_lines> lines of a file
LICENSE_LINES = 7

#: Spack's license identifier
APACHE2_MIT_SPDX = "(Apache-2.0 OR MIT)"

#: regular expressions for licensed files.
LICENSED_FILES = [
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
    r"share/spack/setup-env\.ps1$",
    r"^share/spack/qa/run-[^/]*$",
    r"^share/spack/bash/spack-completion.in$",
    # action workflows
    r"^.github/actions/.*\.py$",
    # all packages
    r"^var/spack/repos/.*/package.py$",
]

#: licensed files that can have LGPL language in them
#: so far, just this command -- so it can find LGPL things elsewhere
LGPL_EXCEPTIONS = [r"lib/spack/spack/cmd/license.py", r"lib/spack/spack/test/cmd/license.py"]


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
    licensed_regex = re.compile("|".join(LICENSED_FILES))
    for relpath in _all_spack_files(args.root):
        if licensed_regex.match(relpath):
            yield relpath


def list_files(args):
    """list files in spack that should have license headers"""
    for relpath in sorted(_licensed_files(args)):
        print(os.path.join(spack.paths.spack_root, relpath))


# Error codes for license verification. All values are chosen such that
# bool(value) evaluates to True
OLD_LICENSE, SPDX_MISMATCH, GENERAL_MISMATCH, EXTRA_COPYRIGHT = range(1, 5)

#: Latest year that copyright applies. UPDATE THIS when bumping copyright.
LATEST_YEAR = datetime.date.today().year
STRICT_DATE = rf"Copyright 2013-{LATEST_YEAR}"

#: regexes for valid license lines at tops of files
LICENSE_LINE_REGEXES = [
    # allow a little leeway: current or last year
    (
        rf"Copyright 2013-({LATEST_YEAR - 1:d}|{LATEST_YEAR:d}) "
        "Lawrence Livermore National Security, LLC and other"
    ),
    r"(Spack|sbang) [Pp]roject [Dd]evelopers\. See the top-level COPYRIGHT file for details.",
    r"SPDX-License-Identifier: \(Apache-2\.0 OR MIT\)",
]


class LicenseError:
    def __init__(self):
        self.error_counts = defaultdict(int)

    def add_error(self, error):
        self.error_counts[error] += 1

    def has_errors(self):
        return sum(self.error_counts.values()) > 0

    def error_messages(self):
        total = sum(self.error_counts.values())
        missing = self.error_counts[GENERAL_MISMATCH]
        spdx_mismatch = self.error_counts[SPDX_MISMATCH]
        old_license = self.error_counts[OLD_LICENSE]
        extra_copyright = self.error_counts[EXTRA_COPYRIGHT]
        return (
            f"{total:d} improperly licensed files",
            f"files with wrong SPDX-License-Identifier:   {spdx_mismatch:d}",
            f"files with old license header:              {old_license:d}",
            f"files with extra Copyright lines:           {extra_copyright:d}",
            f"files not containing expected license:      {missing:d}",
        )


class HeaderExtractor:
    """Extracts the header of a file"""

    comment_character = {r".py": r"#", r".lp": r"%"}

    def __init__(self, file: pathlib.Path) -> None:
        self.file = file

    def extract(self) -> List[str]:
        """Extracts the header from a file, returns a list of lines.

        For Python and clingo files the header is the first block of consecutive comments.
        For other kind of files it's the first LICENSE_LINES lines in the file.
        """
        c = self.comment_character.get(self.file.suffix, None)
        if c is None:
            with open(self.file) as f:
                return [line for line in f][:LICENSE_LINES]

        starts_with_comment = re.compile(rf"^\s*[{c}]")
        result = []
        with open(self.file) as f:
            for line in f:
                if not starts_with_comment.match(line):
                    break
                result.append(line)
        return result


def _check_license(lines, path):
    found, extra_copyright = [], []

    for line in lines:
        line = re.sub(r"^[\s#\%\.\:]*", "", line)
        line = line.rstrip()
        for i, line_regex in enumerate(LICENSE_LINE_REGEXES):
            if re.match(line_regex, line):
                # The first line of the license contains the copyright date.
                # We allow it to be out of date but print a warning if it is
                # out of date.
                if i == 0:
                    if not re.search(STRICT_DATE, line):
                        tty.debug("{0}: copyright date mismatch".format(path))
                found.append(i)
                break

        else:
            if line and "copyright" in line.lower():
                extra_copyright.append(line)

    if (
        len(found) == len(LICENSE_LINE_REGEXES)
        and found == list(sorted(found))
        and not extra_copyright
    ):
        return

    def old_license(line, path):
        if re.search("This program is free software", line):
            print("{0}: has old LGPL license header".format(path))
            return OLD_LICENSE

    # If the SPDX identifier is present, then there is a mismatch (since it
    # did not match the above regex)
    def wrong_spdx_identifier(line, path):
        m = re.search(r"SPDX-License-Identifier: ([^\n]*)", line)
        if m and m.group(1) != APACHE2_MIT_SPDX:
            print(
                "{0}: SPDX license identifier mismatch"
                "(expecting {1}, found {2})".format(path, APACHE2_MIT_SPDX, m.group(1))
            )
            return SPDX_MISMATCH

    checks = [old_license, wrong_spdx_identifier]

    for line in lines:
        for check in checks:
            error = check(line, path)
            if error:
                return error

    if extra_copyright:
        msg = f"{path}:\n\tThe license header has extra Copyright lines, which are not necessary\n"
        msg += "\tSpack contributors always retain copyright, see COPYRIGHT for more information\n"
        msg += "\tExtra copyright lines:\n"
        for line in extra_copyright:
            msg += f"\t\t{line}\n"

        print(msg)
        return EXTRA_COPYRIGHT

    print(f"{path}: the license header at the top of the file does not match the expected format")
    return GENERAL_MISMATCH


def verify(args):
    """verify that files in spack have the right license header"""

    license_errors = LicenseError()

    for relpath in _licensed_files(args):
        path = pathlib.Path(args.root) / relpath
        lines = HeaderExtractor(path).extract()
        error = _check_license(lines, path)
        if error:
            license_errors.add_error(error)

    if license_errors.has_errors():
        tty.die(*license_errors.error_messages())
    else:
        tty.msg("No license issues found.")


def update_copyright_year(args):
    """update copyright for the current year in all licensed files"""

    llns_and_other = " Lawrence Livermore National Security, LLC and other"
    for filename in _licensed_files(args):
        fs.filter_file(
            r"Copyright \d{4}-\d{4}" + llns_and_other,
            STRICT_DATE + llns_and_other,
            os.path.join(args.root, filename),
        )

    # also update MIT license file at root. Don't use llns_and_other; it uses
    # a shortened version of that for better github detection.
    mit_date = STRICT_DATE.replace("Copyright", "Copyright (c)")
    mit_file = os.path.join(args.root, "LICENSE-MIT")
    fs.filter_file(r"Copyright \(c\) \d{4}-\d{4}", mit_date, mit_file)


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
    sp.add_parser("update-copyright-year", help=update_copyright_year.__doc__)


def license(parser, args):
    commands = {
        "list-files": list_files,
        "verify": verify,
        "update-copyright-year": update_copyright_year,
    }
    return commands[args.license_command](args)
