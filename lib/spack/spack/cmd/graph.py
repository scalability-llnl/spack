# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.store
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
        '-s', '--static', action='store_true',
        help="graph static (possible) deps, don't concretize (implies --dot)")

    subparser.add_argument(
        '-i', '--installed', action='store_true',
        help="graph all installed specs in dot format (implies --dot)")

    arguments.add_common_arguments(subparser, ['deptype', 'specs'])


def graph(parser, args):
    if args.installed:
        if args.specs:
            tty.die("Can't specify specs with --installed")
        args.dot = True
        specs = spack.store.store.db.query()

    else:
        specs = spack.cmd.parse_specs(args.specs, concretize=not args.static)

    if not specs:
        setup_parser.parser.print_help()
        return 1

    if args.static:
        args.dot = True

    if args.dot:
        graph_dot(specs, static=args.static, deptype=args.deptype)

    elif specs:  # ascii is default: user doesn't need to provide it explicitly
        debug = spack.config.get('config:debug')
        graph_ascii(specs[0], debug=debug, deptype=args.deptype)
        for spec in specs[1:]:
            print()  # extra line bt/w independent graphs
            graph_ascii(spec, debug=debug)
