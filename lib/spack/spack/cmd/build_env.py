# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.cmd.common.env_utility as env_utility
from spack.context import Context

description = (
    "run a command in a spec's install environment, or dump its environment to screen or file"
)
section = "build"
level = "long"

setup_parser = env_utility.setup_parser


def build_env(parser, args):
    env_utility.emulate_env_utility("build-env", Context.BUILD, args)
