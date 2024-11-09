# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import chmod

from spack.package import *


class Testu01(AutotoolsPackage):
    """TestU01 is a software library, implemented in the ANSI C language, and
    offering a collection of utilities for the empirical statistical testing of
    uniform random number generators."""

    homepage = "http://simul.iro.umontreal.ca/testu01/tu01.html"
    git = "https://github.com/umontreal-simul/TestU01-2009/"

    version(
        "1.2.3",
        sha256="bc1d1dd2aea7ed3b3d28eaad2c8ee55913f11ce67aec8fe4f643c1c0d2ed1cac",
        url="http://simul.iro.umontreal.ca/testu01/TestU01.zip",
    )

    @run_before("configure")
    def fix_permissions(self):
        if not self.force_autoreconf:
            chmod(join_path(self.stage.source_path, "configure"), 0o755)
