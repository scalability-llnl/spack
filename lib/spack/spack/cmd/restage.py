# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
from spack.cmd.common import arguments

description = "revert checked out package source code"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["specs"])


def restage(parser, args):
    if not args.specs:
        tty.die("spack restage requires at least one package spec.")

    specs = spack.cmd.parse_specs(args.specs, concretize=True)
    for spec in specs:
        spec.package.do_restage()
