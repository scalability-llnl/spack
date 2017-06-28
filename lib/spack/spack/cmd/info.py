##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import textwrap
from six.moves import zip_longest
from llnl.util.tty.colify import *
import spack
import spack.fetch_strategy as fs

description = "get detailed information on a particular package"
section = "basic"
level = "short"


def padder(str_list, extra=0):
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * ' ')
    return pad


def setup_parser(subparser):
    subparser.add_argument(
        'name', metavar="PACKAGE", help="name of package to get info for")


class VariantFormatter(object):
    def __init__(self, variants, max_widths=(25, 20, 35)):
        self.variants = variants
        self.headers = ('Name [Default]', 'Allowed values', 'Description')
        # Set max headers lengths
        self.max_column_widths = max_widths

        # Formats
        fmt_name = '{0} [{1}]'

        # Initialize column widths with the length of the
        # corresponding headers, as they cannot be shorter
        # than that
        self.column_widths = [len(x) for x in self.headers]

        # Update according to line lengths
        for k, v in variants.items():
            candidate_max_widths = (
                len(fmt_name.format(k, self.default(v))),  # Name [Default]
                len(v.allowed_values),  # Allowed values
                len(v.description)  # Description
            )

            self.column_widths = (
                max(self.column_widths[0], candidate_max_widths[0]),
                max(self.column_widths[1], candidate_max_widths[1]),
                max(self.column_widths[2], candidate_max_widths[2])
            )

        # Reduce to at most the maximum allowed
        self.column_widths = (
            min(self.column_widths[0], self.max_column_widths[0]),
            min(self.column_widths[1], self.max_column_widths[1]),
            min(self.column_widths[2], self.max_column_widths[2])
        )

        # Compute the format
        self.fmt = "%%-%ss%%-%ss%%s" % (
            self.column_widths[0] + 4,
            self.column_widths[1] + 4
        )

    def default(self, v):
        s = 'on' if v.default is True else 'off'
        if not isinstance(v.default, bool):
            s = v.default
        return s

    @property
    def lines(self):
        if not self.variants:
            yield "    None"
        else:
            yield "    " + self.fmt % self.headers
            yield '\n'
            for k, v in sorted(self.variants.items()):
                name = textwrap.wrap(
                    '{0} [{1}]'.format(k, self.default(v)),
                    width=self.column_widths[0]
                )
                allowed = textwrap.wrap(
                    v.allowed_values,
                    width=self.column_widths[1]
                )
                description = textwrap.wrap(
                    v.description,
                    width=self.column_widths[2]
                )
                for t in zip_longest(
                        name, allowed, description, fillvalue=''
                ):
                    yield "    " + self.fmt % t
                yield ''  # Trigger a new line


def print_text_info(pkg):
    """Print out a plain text description of a package."""
    header = "{0}:   ".format(pkg.build_system_class)

    print(header, pkg.name)

    print()
    print("Description:")
    if pkg.__doc__:
        print(pkg.format_doc(indent=4))
    else:
        print("    None")

    whitespaces = ''.join([' '] * (len(header) - len("Homepage: ")))
    print("Homepage:", whitespaces, pkg.homepage)

    print()
    print("Safe versions:  ")

    if not pkg.versions:
        print("    None")
    else:
        pad = padder(pkg.versions, 4)
        for v in reversed(sorted(pkg.versions)):
            f = fs.for_package_version(pkg, v)
            print("    %s%s" % (pad(v), str(f)))

    print()
    print("Variants:")

    formatter = VariantFormatter(pkg.variants)
    for line in formatter.lines:
        print(line)

    print()
    print("Installation Phases:")
    phase_str = ''
    for phase in pkg.phases:
        phase_str += "    {0}".format(phase)
    print(phase_str)

    for deptype in ('build', 'link', 'run'):
        print()
        print("%s Dependencies:" % deptype.capitalize())
        deps = sorted(pkg.dependencies_of_type(deptype))
        if deps:
            colify(deps, indent=4)
        else:
            print("    None")

    print()
    print("Virtual Packages: ")
    if pkg.provided:
        inverse_map = {}
        for spec, whens in pkg.provided.items():
            for when in whens:
                if when not in inverse_map:
                    inverse_map[when] = set()
                inverse_map[when].add(spec)
        for when, specs in reversed(sorted(inverse_map.items())):
            print("    %s provides %s" % (
                when, ', '.join(str(s) for s in specs)))
    else:
        print("    None")


def info(parser, args):
    pkg = spack.repo.get(args.name)
    print_text_info(pkg)
