# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys
from typing import List

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.confirmation as confirmation
import spack.environment as ev
import spack.spec
from spack.cmd.common import arguments

description = "remove specs from the concretized lockfile of an environment"
section = "environments"
level = "long"

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def setup_parser(subparser):
    subparser.add_argument(
        "--root", action="store_true", help="deconcretize only specific environment roots"
    )
    arguments.add_common_arguments(subparser, ["yes_to_all", "specs"])
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="deconcretize ALL specs that match each supplied spec",
    )


def get_deconcretize_list(
    args: argparse.Namespace, specs: List[spack.spec.Spec], env: ev.Environment
) -> List[spack.spec.Spec]:
    """
    Get list of environment roots to deconcretize
    """
    env_specs = [s for _, s in env.concretized_specs()]
    to_deconcretize = []
    errors = []

    for s in specs:
        if args.root:
            # find all roots matching given spec
            to_deconc = [e for e in env_specs if e.satisfies(s)]
        else:
            # find all roots matching or depending on a matching spec
            to_deconc = [e for e in env_specs if any(d.satisfies(s) for d in e.traverse())]

        if len(to_deconc) < 1:
            tty.warn(f"No matching specs to deconcretize for {s}")

        elif len(to_deconc) > 1 and not args.all:
            errors.append((s, to_deconc))

        to_deconcretize.extend(to_deconc)

    if errors:
        for spec, matching in errors:
            tty.error(f"{spec} matches multiple concrete specs:")
            sys.stderr.write("\n")
            spack.cmd.display_specs(matching, output=sys.stderr, **display_args)
            sys.stderr.write("\n")
            sys.stderr.flush()
        tty.die("Use '--all' to deconcretize all matching specs, or be more specific")

    return to_deconcretize


def deconcretize_specs(args, specs):
    env = spack.cmd.require_active_env(cmd_name="deconcretize")

    if args.specs:
        deconcretize_list = get_deconcretize_list(args, specs, env)
    else:
        deconcretize_list = [s for _, s in env.concretized_specs()]

    if not args.yes_to_all:
        confirmation.confirm_action(deconcretize_list, "deconcretized", "deconcretization")

    with env.write_transaction():
        for spec in deconcretize_list:
            env.deconcretize(spec)
        env.write()


def deconcretize(parser, args):
    if not args.specs and not args.all:
        tty.die(
            "deconcretize requires at least one spec argument.",
            " Use `spack deconcretize --all` to deconcretize ALL specs.",
        )

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    deconcretize_specs(args, specs)
