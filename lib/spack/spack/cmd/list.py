##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import sys
import llnl.util.tty as tty
import argparse
from llnl.util.tty.colify import colify

import spack
import fnmatch
import re

description = "List available spack packages"


def setup_parser(subparser):
    subparser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='Optional glob patterns to filter results.')
    subparser.add_argument(
        '-s', '--sensitive', action='store_true', default=False,
        help='Use case-sensitive filtering. Default is case sensitive, '
        'unless the query contains a capital letter.')
    subparser.add_argument(
        '-d', '--search-description', action='store_true', default=False,
        help='Filtering will also search the description for a match.')


def list(parser, args):
    # Start with all package names.
    pkgs = set(spack.repo.all_package_names())

    # filter if a filter arg was provided
    if args.filter:
        res = []
        for f in args.filter:
            if '*' not in f and '?' not in f:
                r = fnmatch.translate('*' + f + '*')
            else:
                r = fnmatch.translate(f)

            re_flags = re.I
            if any(l.isupper for l in f) or args.sensitive:
                re_flags = 0
            rc = re.compile(r, flags=re_flags)
            res.append(rc)

        if args.search_description:
            def match(p, f):
                if f.match(p):
                    return True

                pkg = spack.repo.get(p)
                if pkg.__doc__:
                    return f.match(pkg.__doc__)
                return False
        else:
            def match(p, f):
                return f.match(p)
        pkgs = [p for p in pkgs if any(match(p, f) for f in res)]

    # sort before displaying.
    sorted_packages = sorted(pkgs, key=lambda s: s.lower())

    # Print all the package names in columns
    indent = 0
    if sys.stdout.isatty():
        tty.msg("%d packages." % len(sorted_packages))
    colify(sorted_packages, indent=indent)
