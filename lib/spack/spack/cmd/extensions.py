# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.cmd as cmd
import spack.environment as ev
import spack.repo
import spack.store
from spack.cmd.common import arguments

description = "list extensions for package"
section = "extensions"
level = "long"


def setup_parser(subparser):
    subparser.epilog = (
        "If called without argument returns the list of all valid extendable packages"
    )
    arguments.add_common_arguments(subparser, ["long", "very_long"])
    subparser.add_argument(
        "-d", "--deps", action="store_true", help="output dependencies along with found specs"
    )

    subparser.add_argument(
        "-p", "--paths", action="store_true", help="show paths to package install directories"
    )
    subparser.add_argument(
        "-s",
        "--show",
        action="store",
        default="all",
        choices=("packages", "installed", "all"),
        help="show only part of output",
    )

    subparser.add_argument(
        "spec",
        nargs=argparse.REMAINDER,
        help="spec of package to list extensions for",
        metavar="extendable",
    )


def extensions(parser, args):
    if not args.spec:
        # If called without arguments, list all the extendable packages
        isatty = sys.stdout.isatty()
        if isatty:
            tty.info("Extendable packages:")

        extendable_pkgs = []
        for name in spack.repo.all_package_names():
            pkg_cls = spack.repo.PATH.get_pkg_class(name)
            if pkg_cls.extendable:
                extendable_pkgs.append(name)

        colify(extendable_pkgs, indent=4)
        return

    # Checks
    spec = cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("Can only list extensions for one package.")

    env = ev.active_environment()
    spec = cmd.disambiguate_spec(spec[0], env)

    if not spec.package.extendable:
        tty.die("%s is not an extendable package." % spec.name)

    if not spec.package.extendable:
        tty.die("%s does not have extensions." % spec.short_spec)

    if args.show in ("packages", "all"):
        # List package names of extensions
        extensions = spack.repo.PATH.extensions_for(spec)
        if not extensions:
            tty.msg("%s has no extensions." % spec.cshort_spec)
        else:
            tty.msg(spec.cshort_spec)
            tty.msg("%d extensions:" % len(extensions))
            colify(ext.name for ext in extensions)

    if args.show in ("installed", "all"):
        # List specs of installed extensions.
        installed = [s.spec for s in spack.store.STORE.db.installed_extensions_for(spec)]

        if args.show == "all":
            print
        if not installed:
            tty.msg("None installed.")
        else:
            tty.msg("%d installed:" % len(installed))
            cmd.display_specs(installed, args)
