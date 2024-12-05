# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sph2pipe(CMakePackage):
    """Sph2pipe is a portable tool for
    converting SPHERE files to other formats."""

    homepage = "https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools"
    url = "https://www.ldc.upenn.edu/sites/default/files/sph2pipe_v2.5.tar.gz"

    version("2.5", sha256="5be236dc94ed0a301c5c8a369f849f76799ec7e70f25dfc0521068d9d1d4d3e3")

    depends_on("c", type="build")  # generated

    patch("cmake.patch")
