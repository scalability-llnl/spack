# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util import tty

import spack.config

description = "toggle metrics collection"
section = "admin"
level = "long"


def setup_parser(subparser):
    metrics_cmd_group = subparser.add_mutually_exclusive_group()
    metrics_cmd_group.add_argument('metrics_toggle',
                                   nargs='?',
                                   default=None,
                                   help='enable/disable')
    metrics_cmd_group.add_argument('--set-path',
                                   dest='metrics_address',
                                   help="""set path where
                                           metrics are logged to""")


def metrics(parser, args):

    if args.metrics_address:
        spack.config.set('config:metrics_address',
                         args.metrics_address,
                         "site")
        return 0

    if args.metrics_toggle == "enable":
        spack.config.set('config:metrics', True, scope='site')
    elif args.metrics_toggle == "disable":
        spack.config.set('config:metrics', False, scope='site')
    else:
        tty.die("Error: Unrecognized Option: %s" % args.metrics_toggle)
