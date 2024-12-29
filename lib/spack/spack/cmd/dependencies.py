# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.environment as ev
import spack.package_base
import spack.store
from spack.cmd.common import arguments

description = "show dependencies of a package"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-i",
        "--installed",
        action="store_true",
        default=False,
        help="list installed dependencies of an installed spec "
        "instead of possible dependencies of a package",
    )
    subparser.add_argument(
        "-t",
        "--transitive",
        action="store_true",
        default=False,
        help="show all transitive dependencies",
    )
    arguments.add_common_arguments(subparser, ["deptype"])
    subparser.add_argument(
        "-V",
        "--no-expand-virtuals",
        action="store_false",
        default=True,
        dest="expand_virtuals",
        help="do not expand virtual dependencies",
    )
    arguments.add_common_arguments(subparser, ["spec"])


def dependencies(parser, args):
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("spack dependencies takes only one spec.")

    if args.installed:
        env = ev.active_environment()
        spec = spack.cmd.disambiguate_spec(specs[0], env)

        format_string = "{name}{@version}{%compiler}{/hash:7}"
        if sys.stdout.isatty():
            tty.msg("Dependencies of %s" % spec.format(format_string, color=True))
        deps = spack.store.STORE.db.installed_relatives(
            spec, "children", args.transitive, deptype=args.deptype
        )
        if deps:
            spack.cmd.display_specs(deps, long=True)
        else:
            print("No dependencies")

    else:
        spec = specs[0]
        dependencies = spack.package_base.possible_dependencies(
            spec,
            transitive=args.transitive,
            expand_virtuals=args.expand_virtuals,
            depflag=args.deptype,
        )

        if spec.name in dependencies:
            del dependencies[spec.name]

        if dependencies:
            colify(sorted(dependencies))
        else:
            print("No dependencies")
