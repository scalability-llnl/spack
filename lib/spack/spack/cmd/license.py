# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime
import os
import re
from collections import defaultdict

import llnl.util.filesystem as fs
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
lgpl_exceptions = [r"lib/spack/spack/cmd/license.py", r"lib/spack/spack/test/cmd/license.py"]


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
OLD_LICENSE, SPDX_MISMATCH, GENERAL_MISMATCH = range(1, 4)

#: Latest year that copyright applies. UPDATE THIS when bumping copyright.
latest_year = datetime.date.today().year
strict_date = r"Copyright 2013-%s" % latest_year

#: regexes for valid license lines at tops of files
license_line_regexes = [
    r"Copyright 2013-(%d|%d) Lawrence Livermore National Security, LLC and other"
    % (latest_year - 1, latest_year),  # allow a little leeway: current or last year
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
        return (
            "%d improperly licensed files" % (total),
            "files with wrong SPDX-License-Identifier:   %d" % spdx_mismatch,
            "files with old license header:              %d" % old_license,
            "files not containing expected license:      %d" % missing,
        )


def _check_license(lines, path):
    found = []

    for line in lines:
        line = re.sub(r"^[\s#\%\.\:]*", "", line)
        line = line.rstrip()
        for i, line_regex in enumerate(license_line_regexes):
            if re.match(line_regex, line):
                # The first line of the license contains the copyright date.
                # We allow it to be out of date but print a warning if it is
                # out of date.
                if i == 0:
                    if not re.search(strict_date, line):
                        tty.debug("{0}: copyright date mismatch".format(path))
                found.append(i)

    if len(found) == len(license_line_regexes) and found == list(sorted(found)):
        return

    def old_license(line, path):
        if re.search("This program is free software", line):
            print("{0}: has old LGPL license header".format(path))
            return OLD_LICENSE

    # If the SPDX identifier is present, then there is a mismatch (since it
    # did not match the above regex)
    def wrong_spdx_identifier(line, path):
        m = re.search(r"SPDX-License-Identifier: ([^\n]*)", line)
        if m and m.group(1) != apache2_mit_spdx:
            print(
                "{0}: SPDX license identifier mismatch"
                "(expecting {1}, found {2})".format(path, apache2_mit_spdx, m.group(1))
            )
            return SPDX_MISMATCH

    checks = [old_license, wrong_spdx_identifier]

    for line in lines:
        for check in checks:
            error = check(line, path)
            if error:
                return error

    print(
        "{0}: the license header at the top of the file does not match the \
          expected format".format(
            path
        )
    )
    return GENERAL_MISMATCH


def verify(args):
    """verify that files in spack have the right license header"""

    license_errors = LicenseError()

    for relpath in _licensed_files(args):
        path = os.path.join(args.root, relpath)
        with open(path) as f:
            lines = [line for line in f][:license_lines]

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
            strict_date + llns_and_other,
            os.path.join(args.root, filename),
        )

    # also update MIT license file at root. Don't use llns_and_other; it uses
    # a shortened version of that for better github detection.
    mit_date = strict_date.replace("Copyright", "Copyright (c)")
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
    licensed_files[:] = [re.compile(regex) for regex in licensed_files]

    commands = {
        "list-files": list_files,
        "verify": verify,
        "update-copyright-year": update_copyright_year,
    }
    return commands[args.license_command](args)
