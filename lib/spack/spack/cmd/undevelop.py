# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.cmd.common.deployment as deployment
import spack.environment as ev


description = 'remove development information from an environment'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="remove all specs from (clear) the environment")
    arguments.add_common_arguments(subparser, ['specs'])


def undevelop(parser, args):
    deployment.die_if_deployment('undevelop')

    env = ev.get_env(args, 'undevelop', required=True)

    if args.all:
        specs = env.dev_specs.keys()
    else:
        specs = spack.cmd.parse_specs(args.specs)

    with env.write_transaction():
        changed = False
        for spec in specs:
            tty.msg('Removing %s from environment %s development specs'
                    % (spec, env.name))
            changed |= env.undevelop(spec)
        if changed:
            env.write()
