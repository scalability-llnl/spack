# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModuleManpathSetenv(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/module-manpath-setenv-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env):
        env.set("MANPATH", "/path/to/man")
