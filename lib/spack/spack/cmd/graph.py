##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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

import argparse
import llnl.util.tty as tty

import spack
import spack.cmd
import spack.store
from spack.dependency import canonical_deptype
from spack.graph import graph_dot, graph_ascii

description = "generate graphs of package dependency relationships"
section = "basic"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser

    method = subparser.add_mutually_exclusive_group()
    method.add_argument(
        '-a', '--ascii', action='store_true',
        help="draw graph as ascii to stdout (default)")
    method.add_argument(
        '-d', '--dot', action='store_true',
        help="generate graph in dot format and print to stdout")

    subparser.add_argument(
        '-n', '--normalize', action='store_true',
        help="skip concretization; only print normalized spec")

    subparser.add_argument(
        '-s', '--static', action='store_true',
        help="use static information from packages, not dynamic spec info")

    subparser.add_argument(
        '-i', '--installed', action='store_true',
        help="graph all installed specs in dot format (implies --dot)")

    subparser.add_argument(
        '-t', '--deptype', action='store',
        help="comma-separated list of deptypes to traverse. default=%s"
        % ','.join(('link', 'run')))

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="specs of packages to graph")


def graph(parser, args):
    concretize = not args.normalize
    if args.installed:
        if args.specs:
            tty.die("Can't specify specs with --installed")
        args.dot = True
        specs = spack.store.db.query()

    else:
        specs = spack.cmd.parse_specs(
            args.specs, normalize=True, concretize=concretize)

    if not specs:
        setup_parser.parser.print_help()
        return 1

    deptype = ('link', 'run')
    if args.deptype:
        deptype = tuple(args.deptype.split(','))
        if deptype == ('all',):
            deptype = 'all'
        deptype = canonical_deptype(deptype)

    if args.dot:  # Dot graph only if asked for.
        graph_dot(specs, static=args.static, deptype=deptype)

    elif specs:  # ascii is default: user doesn't need to provide it explicitly
        graph_ascii(specs[0], debug=spack.debug, deptype=deptype)
        for spec in specs[1:]:
            print()  # extra line bt/w independent graphs
            graph_ascii(spec, debug=spack.debug)
