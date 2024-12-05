# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.cmd.common
import spack.cmd.location

description = "cd to spack directories in the shell"
section = "developer"
level = "long"


def setup_parser(subparser):
    """This is for decoration -- spack cd is used through spack's
    shell support.  This allows spack cd to print a descriptive
    help message when called with -h."""
    spack.cmd.location.setup_parser(subparser)


def cd(parser, args):
    spec = " ".join(args.spec) if args.spec else "SPEC"
    spack.cmd.common.shell_init_instructions(
        "spack cd", "cd `spack location --install-dir %s`" % spec
    )
