# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import mkdirp

import spack.install_scheme

description = "Update Spack to stop writing into its own prefix"
section = "build"
level = "long"


def setup_parser(subparser):
    pass


def read_only_core(parser, args):
    config_dir = spack.install_scheme.config(for_alias="out-of-spack")

    mkdirp(config_dir)
