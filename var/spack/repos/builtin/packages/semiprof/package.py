# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Semiprof(CMakePackage):
    """Simple thread safe annotation based C++ profiler."""

    homepage = "https://github.com/bcumming/semiprof"
    url = "https://github.com/bcumming/semiprof/archive/refs/tags/v0.1.tar.gz"

    maintainers("simonpintarelli")

    variant("examples", default=False, description="Enable examples")
    variant("shared", default=True, description="Build shared libraries")

    license("BSD-3-Clause")

    version("0.1", sha256="4fb3823c65a4f5dfbe05e8cbe1911dfd25cd7740597f82c7b3a84472de26f0dc")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        return [
            self.define("SEMIPROF_WITH_INSTALL", True),
            self.define_from_variant("SEMIPROF_WITH_EXAMPLES", "examples"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
