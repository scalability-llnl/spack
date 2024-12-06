# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
from spack.cmd.common import arguments

description = "add a spec to an environment"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-l",
        "--list-name",
        dest="list_name",
        default="specs",
        help="name of the list to add specs to",
    )
    arguments.add_common_arguments(subparser, ["specs"])


def add(parser, args):
    env = spack.cmd.require_active_env(cmd_name="add")

    with env.write_transaction():
        for spec in spack.cmd.parse_specs(args.specs):
            if not env.add(spec, args.list_name):
                tty.msg("Package {0} was already added to {1}".format(spec.name, env.name))
            else:
                tty.msg("Adding %s to environment %s" % (spec, env.name))
        env.write()
