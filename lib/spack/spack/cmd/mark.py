# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from llnl.util import tty

import spack.cmd
import spack.store
from spack.cmd.common import arguments
from spack.database import InstallStatuses

description = "mark packages as explicitly or implicitly installed"
section = "admin"
level = "long"

error_message = """You can either:
    a) use a more specific spec, or
    b) use `spack mark --all` to mark ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["installed_specs"])
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="mark ALL installed packages that match each supplied spec",
    )
    exim = subparser.add_mutually_exclusive_group(required=True)
    exim.add_argument(
        "-e",
        "--explicit",
        action="store_true",
        dest="explicit",
        help="mark packages as explicitly installed",
    )
    exim.add_argument(
        "-i",
        "--implicit",
        action="store_true",
        dest="implicit",
        help="mark packages as implicitly installed",
    )


def find_matching_specs(specs, allow_multiple_matches=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        specs (list): list of specs to be matched against installed packages
        allow_multiple_matches (bool): if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False

    for spec in specs:
        install_query = [InstallStatuses.INSTALLED]
        matching = spack.store.STORE.db.query_local(spec, installed=install_query)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error("{0} matches multiple packages:".format(spec))
            sys.stderr.write("\n")
            spack.cmd.display_specs(matching, output=sys.stderr, **display_args)
            sys.stderr.write("\n")
            sys.stderr.flush()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.die("{0} does not match any installed packages.".format(spec))

        specs_from_cli.extend(matching)

    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def do_mark(specs, explicit):
    """Marks all the specs in a list.

    Args:
        specs (list): list of specs to be marked
        explicit (bool): whether to mark specs as explicitly installed
    """
    for spec in specs:
        spack.store.STORE.db.update_explicit(spec, explicit)


def mark_specs(args, specs):
    mark_list = find_matching_specs(specs, args.all)

    # Mark everything on the list
    do_mark(mark_list, args.explicit)


def mark(parser, args):
    if not args.specs and not args.all:
        tty.die(
            "mark requires at least one package argument.",
            "  Use `spack mark --all` to mark ALL packages.",
        )

    # [any] here handles the --all case by forcing all specs to be returned
    specs = spack.cmd.parse_specs(args.specs) if args.specs else [any]
    mark_specs(args, specs)
