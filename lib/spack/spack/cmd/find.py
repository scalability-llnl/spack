# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty
import llnl.util.lang

import spack.repo
import spack.cmd.common.arguments as arguments
from spack.cmd import display_specs

description = "list and search installed packages"
section = "basic"
level = "short"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument('-s', '--short',
                              action='store_const',
                              dest='mode',
                              const='short',
                              default='short',
                              help='show only specs (default)')
    format_group.add_argument('-p', '--paths',
                              action='store_const',
                              dest='mode',
                              const='paths',
                              help='show paths to package install directories')
    format_group.add_argument(
        '-d', '--deps',
        action='store_const',
        dest='mode',
        const='deps',
        help='show full dependency DAG of installed packages')

    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'tags'])

    subparser.add_argument('-f', '--show-flags',
                           action='store_true',
                           dest='show_flags',
                           help='show spec compiler flags')
    subparser.add_argument('--show-full-compiler',
                           action='store_true',
                           dest='show_full_compiler',
                           help='show full compiler specs')
    implicit_explicit = subparser.add_mutually_exclusive_group()
    implicit_explicit.add_argument(
        '-x', '--explicit',
        action='store_true',
        help='show only specs that were installed explicitly')
    implicit_explicit.add_argument(
        '-X', '--implicit',
        action='store_true',
        help='show only specs that were installed as dependencies')
    subparser.add_argument(
        '-u', '--unknown',
        action='store_true',
        dest='unknown',
        help='show only specs Spack does not have a package for')
    subparser.add_argument(
        '-m', '--missing',
        action='store_true',
        dest='missing',
        help='show missing dependencies as well as installed specs')
    subparser.add_argument(
        '-v', '--variants',
        action='store_true',
        dest='variants',
        help='show variants in output (can be long)')
    subparser.add_argument('-M', '--only-missing',
                           action='store_true',
                           dest='only_missing',
                           help='show only missing dependencies')
    subparser.add_argument('-N', '--namespace',
                           action='store_true',
                           help='show fully qualified package names')

    subparser.add_argument(
        '--start-date',
        help='earliest date of installation [YYYY-MM-DD]'
    )
    subparser.add_argument(
        '--end-date', help='latest date of installation [YYYY-MM-DD]'
    )

    arguments.add_common_arguments(subparser, ['constraint'])


def query_arguments(args):
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

    # Time window of installation
    for attribute in ('start_date', 'end_date'):
        date = getattr(args, attribute)
        if date:
            q_args[attribute] = llnl.util.lang.pretty_string_to_date(date)

    return q_args


def find(parser, args):
    q_args = query_arguments(args)
    query_specs = args.specs(**q_args)

    # Exit early if no package matches the constraint
    if not query_specs and args.constraint:
        msg = "No package matches the query: {0}"
        msg = msg.format(' '.join(args.constraint))
        tty.msg(msg)
        return

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.path.packages_with_tags(*args.tags)
        query_specs = [x for x in query_specs if x.name in packages_with_tags]

    # Display the result
    if sys.stdout.isatty():
        tty.msg("%d installed packages." % len(query_specs))

    display_specs(query_specs, args)
