# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.environment as ev
from spack.spec import Spec

description = 'Concretize an environment and write a lockfile.'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    subparser.add_argument(
        '-d', '--dry-run', action='store_true', default=False,
        help="(Re-)concretize, but don't generate the lockfile.")
    subparser.epilog = (
        'Statuses: {s.POS_STATUS} - installed, '
        '{s.NEG_STATUS} - not installed, \n'
        '          {s.UPSTREAM_STATUS} - upstream,  '
        '{s.ERR_STATUS} - install missing/error'
        .format(s=Spec))


def concretize(parser, args):
    env = ev.get_env(args, 'concretize', required=True)
    with env.write_transaction():
        concretized_specs = env.concretize(force=args.force or args.dry_run)
        ev.display_specs(concretized_specs)

        if not args.dry_run:
            env.write()
