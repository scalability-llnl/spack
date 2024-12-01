# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModuleLongHelp(Package):
    """Package to test long description message generated in modulefile.
    Message too long is wrapped over multiple lines."""

    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/module-long-help-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env):
        env.set("FOO", "bar")
