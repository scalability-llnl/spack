# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gnuconfig(Package):
    """
    The GNU config.guess and config.sub scripts versioned by timestamp.
    This package can be used as a build dependency for autotools packages that
    ship a tarball with outdated config.guess and config.sub files.
    """

    has_code = False

    version("2021-08-14")

    def install(self, spec, prefix):
        config_sub = join_path(prefix, "config.sub")
        config_guess = join_path(prefix, "config.guess")

        # Create files
        with open(config_sub, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\necho gnuconfig version of config.sub")

        with open(config_guess, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\necho gnuconfig version of config.guess")

        # Make executable
        os.chmod(config_sub, 0o775)
        os.chmod(config_guess, 0o775)
