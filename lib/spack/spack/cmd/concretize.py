# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.environment as ev

description = 'concretize an environment and write a lockfile'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    subparser.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""Concretize with test dependencies. When 'root' is chosen, test
dependencies are only added for the environment's root specs. When 'all' is
chosen, test dependencies are enabled for all packages in the environment.""")


def concretize(parser, args):
    env = ev.get_env(args, 'concretize', required=True)

    if args.test == 'all':
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in env.user_specs]
    else:
        tests = False

    with env.write_transaction():
        concretized_specs = env.concretize(force=args.force, tests=tests)
        ev.display_specs(concretized_specs)
        env.write()
