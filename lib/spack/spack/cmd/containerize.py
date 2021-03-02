# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path

import llnl.util.tty
import spack.container
import spack.container.images

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--list-os', action='store_true', default=False,
        help='list all the OS that can be used in the bootstrap phase and exit'
    )
    stages = subparser.add_mutually_exclusive_group()
    stages.add_argument(
        '--bootstrap', action='store_true', default=False,
        help='print only the bootstrap phase in a recipe'
    )
    stages.add_argument(
        '--build', action='store_true', default=False,
        help='print only the bootstrap and build phases in a recipe'
    )


def containerize(parser, args):
    if args.list_os:
        possible_os = spack.container.images.all_bootstrap_os()
        msg = 'The following operating systems can be used to bootstrap Spack:'
        msg += '\n{0}'.format(' '.join(possible_os))
        llnl.util.tty.msg(msg)
        return

    config_dir = args.env_dir or os.getcwd()
    config_file = os.path.abspath(os.path.join(config_dir, 'spack.yaml'))
    if not os.path.exists(config_file):
        msg = 'file not found: {0}'
        raise ValueError(msg.format(config_file))

    config = spack.container.validate(config_file)

    last_phase = None
    if args.bootstrap:
        last_phase = 'bootstrap'
    elif args.build:
        last_phase = 'build'

    recipe = spack.container.recipe(config, last_phase=last_phase)
    print(recipe)
