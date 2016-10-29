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
import argparse
import sys

import llnl.util.tty as tty
import spack
import spack.spec
import spack.store
from llnl.util.lang import *
from llnl.util.tty.colify import *
from llnl.util.tty.color import *
from spack.cmd import display_specs

description = "Find installed spack packages"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument('-s', '--short',
                              action='store_const',
                              dest='mode',
                              const='short',
                              help='Show only specs (default)')
    format_group.add_argument('-p', '--paths',
                              action='store_const',
                              dest='mode',
                              const='paths',
                              help='Show paths to package install directories')
    format_group.add_argument(
        '-d', '--deps',
        action='store_const',
        dest='mode',
        const='deps',
        help='Show full dependency DAG of installed packages')

    subparser.add_argument('-l', '--long',
                           action='store_true',
                           dest='long',
                           help='Show dependency hashes as well as versions.')
    subparser.add_argument('-L', '--very-long',
                           action='store_true',
                           dest='very_long',
                           help='Show dependency hashes as well as versions.')
    subparser.add_argument('-f', '--show-flags',
                           action='store_true',
                           dest='show_flags',
                           help='Show spec compiler flags.')

    subparser.add_argument(
        '-e', '--explicit',
        action='store_true',
        help='Show only specs that were installed explicitly')
    subparser.add_argument(
        '-E', '--implicit',
        action='store_true',
        help='Show only specs that were installed as dependencies')
    subparser.add_argument(
        '-u', '--unknown',
        action='store_true',
        dest='unknown',
        help='Show only specs Spack does not have a package for.')
    subparser.add_argument(
        '-m', '--missing',
        action='store_true',
        dest='missing',
        help='Show missing dependencies as well as installed specs.')
    subparser.add_argument(
        '-v', '--variants',
        action='store_true',
        dest='variants',
        help='Show variants in output (can be long)')
    subparser.add_argument('-M', '--only-missing',
                           action='store_true',
                           dest='only_missing',
                           help='Show only missing dependencies.')
    subparser.add_argument('-N', '--namespace',
                           action='store_true',
                           help='Show fully qualified package names.')

    subparser.add_argument('query_specs',
                           nargs=argparse.REMAINDER,
                           help='optional specs to filter results')


def query_arguments(args):
    # Check arguments
    if args.explicit and args.implicit:
        tty.error('You can\'t pass -E and -e options simultaneously.')
        raise SystemExit(1)

    # Set up query arguments.
    installed, known = True, any
    if args.only_missing:
        installed = False
    elif args.missing:
        installed = any
    if args.unknown:
        known = False
    explicit = any
    if args.explicit:
        explicit = True
    if args.implicit:
        explicit = False
    q_args = {'installed': installed, 'known': known, "explicit": explicit}
    return q_args


def find(parser, args):
    # Filter out specs that don't exist.
    query_specs = spack.cmd.parse_specs(args.query_specs)
    query_specs, nonexisting = partition_list(
        query_specs, lambda s: spack.repo.exists(s.name) or not s.name)

    if nonexisting:
        msg = "No such package%s: " % ('s' if len(nonexisting) > 1 else '')
        msg += ", ".join(s.name for s in nonexisting)
        tty.msg(msg)

        if not query_specs:
            return

    q_args = query_arguments(args)

    # Get all the specs the user asked for
    if not query_specs:
        specs = set(spack.store.db.query(**q_args))
    else:
        results = [set(spack.store.db.query(qs, **q_args))
                   for qs in query_specs]
        specs = set.union(*results)

    if not args.mode:
        args.mode = 'short'

    if sys.stdout.isatty():
        tty.msg("%d installed packages." % len(specs))
    display_specs(specs,
                  mode=args.mode,
                  long=args.long,
                  very_long=args.very_long,
                  show_flags=args.show_flags,
                  namespace=args.namespace,
                  variants=args.variants)
