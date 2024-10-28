# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Deprecate one Spack install in favor of another

Spack packages of different configurations cannot be installed to the same
location. However, in some circumstances (e.g. security patches) old
installations should never be used again. In these cases, we will mark the old
installation as deprecated, remove it, and link another installation into its
place.

It is up to the user to ensure binary compatibility between the deprecated
installation and its deprecator.
"""
import argparse

import llnl.util.tty as tty
from llnl.util.symlink import symlink

import spack.cmd
import spack.environment as ev
import spack.installer
import spack.store
from spack.cmd.common import arguments
from spack.database import InstallStatuses
from spack.error import SpackError

description = "replace one package with another via symlinks"
section = "admin"
level = "long"

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": True, "variants": True, "indent": 4}


def setup_parser(sp):
    setup_parser.parser = sp

    arguments.add_common_arguments(sp, ["yes_to_all"])

    deps = sp.add_mutually_exclusive_group()
    deps.add_argument(
        "-d",
        "--dependencies",
        action="store_true",
        default=True,
        dest="dependencies",
        help="deprecate dependencies (default)",
    )
    deps.add_argument(
        "-D",
        "--no-dependencies",
        action="store_false",
        default=True,
        dest="dependencies",
        help="do not deprecate dependencies",
    )

    install = sp.add_mutually_exclusive_group()
    install.add_argument(
        "-i",
        "--install-deprecator",
        action="store_true",
        default=False,
        dest="install",
        help="concretize and install deprecator spec",
    )
    install.add_argument(
        "-I",
        "--no-install-deprecator",
        action="store_false",
        default=False,
        dest="install",
        help="deprecator spec must already be installed (default)",
    )

    sp.add_argument(
        "-l", "--link-type", type=str, default=None, choices=["soft", "hard"], help="(deprecated)"
    )

    sp.add_argument(
        "specs", nargs=argparse.REMAINDER, help="spec to deprecate and spec to use as deprecator"
    )


def deprecate(parser, args):
    """Deprecate one spec in favor of another"""
    if args.link_type is not None:
        tty.warn("The --link-type option is deprecated and will be removed in a future release.")

    env = ev.active_environment()
    specs = spack.cmd.parse_specs(args.specs)

    if len(specs) != 2:
        raise SpackError("spack deprecate requires exactly two specs")

    install_query = [InstallStatuses.INSTALLED, InstallStatuses.DEPRECATED]
    deprecate = spack.cmd.disambiguate_spec(specs[0], env, local=True, installed=install_query)

    if args.install:
        deprecator = specs[1].concretized()
    else:
        deprecator = spack.cmd.disambiguate_spec(specs[1], env, local=True)

    # calculate all deprecation pairs for errors and warning message
    all_deprecate = []
    all_deprecators = []

    generator = (
        deprecate.traverse(order="post", deptype="link", root=True)
        if args.dependencies
        else [deprecate]
    )
    for spec in generator:
        all_deprecate.append(spec)
        all_deprecators.append(deprecator[spec.name])
        # This will throw a key error if deprecator does not have a dep
        # that matches the name of a dep of the spec

    if not args.yes_to_all:
        tty.msg("The following packages will be deprecated:\n")
        spack.cmd.display_specs(all_deprecate, **display_args)
        tty.msg("In favor of (respectively):\n")
        spack.cmd.display_specs(all_deprecators, **display_args)
        print()

        already_deprecated = []
        already_deprecated_for = []
        for spec in all_deprecate:
            deprecated_for = spack.store.STORE.db.deprecator(spec)
            if deprecated_for:
                already_deprecated.append(spec)
                already_deprecated_for.append(deprecated_for)

        tty.msg("The following packages are already deprecated:\n")
        spack.cmd.display_specs(already_deprecated, **display_args)
        tty.msg("In favor of (respectively):\n")
        spack.cmd.display_specs(already_deprecated_for, **display_args)

        answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
        if not answer:
            tty.die("Will not deprecate any packages.")

    for dcate, dcator in zip(all_deprecate, all_deprecators):
        spack.installer.deprecate(dcate, dcator, symlink)
