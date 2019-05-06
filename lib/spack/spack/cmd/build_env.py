# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import os
import shlex

import llnl.util.tty as tty
import spack.build_environment as build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments

description = "show install environment for a spec, and run commands"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['clean', 'dirty'])
    subparser.add_argument(
        '-c', '--command', dest='build_command', default=None,
        help="command to run in the build environment")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs of package environment to emulate")


def build_env(parser, args):
    if not args.spec:
        tty.die("spack build-env requires a spec.")

    specs = spack.cmd.parse_specs(args.spec, concretize=True)
    if len(specs) > 1:
        tty.die("spack build-env only takes one spec.")
    spec = specs[0]

    build_environment.setup_package(spec.package, args.dirty)

    if not args.build_command:
        # If no command act like the "env" command and print out env vars.
        for key, val in os.environ.items():
            print('{0}={1}'.format(key, val))
    else:
        # Otherwise execute the command with the new environment
        cmd = shlex.split(args.build_command)
        os.execvp(cmd[0], cmd)
