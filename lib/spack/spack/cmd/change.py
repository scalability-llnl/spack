# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.cmd
import spack.spec
from spack.cmd.common import arguments

description = "change an existing spec in an environment"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-l",
        "--list-name",
        dest="list_name",
        default="specs",
        help="name of the list to remove specs from",
    )
    subparser.add_argument(
        "--match-spec", dest="match_spec", help="if name is ambiguous, supply a spec to match"
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="change all matching specs (allow changing more than one spec)",
    )
    arguments.add_common_arguments(subparser, ["specs"])


def change(parser, args):
    env = spack.cmd.require_active_env(cmd_name="change")

    with env.write_transaction():
        if args.match_spec:
            match_spec = spack.spec.Spec(args.match_spec)
        else:
            match_spec = None
        for spec in spack.cmd.parse_specs(args.specs):
            env.change_existing_spec(
                spec,
                list_name=args.list_name,
                match_spec=match_spec,
                allow_changing_multiple_specs=args.all,
            )
        env.write()
