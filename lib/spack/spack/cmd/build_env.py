# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.cmd.common.env_utility as env_utility
from spack.context import Context

description = (
    "use a spec's build environment to run a command, dump to screen or file, or dive into it"
)
section = "build"
level = "long"

setup_parser = env_utility.setup_parser


def build_env(parser, args):
    env_utility.emulate_env_utility("build-env", Context.BUILD, args)
