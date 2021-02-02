# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.cmd.common.deployment as deployment
import spack.cmd.common.env_utility as env_utility

description = "run a command in a spec's test environment, " \
              "or dump its environment to screen or file"
section = "admin"
level = "long"

setup_parser = env_utility.setup_parser


def test_env(parser, args):
    deployment.die_if_deployment('test-env')
    env_utility.emulate_env_utility('test-env', 'test', args)
