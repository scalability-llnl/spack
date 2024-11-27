# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qoz(CMakePackage):
    """Quality optimized version of SZ3 is the next generation of the SZ compressor framework"""

    git = "https://github.com/robertu94/QoZ"
    homepage = git

    version("2023.11.07", commit="611369be4b1cc7a12eaae02600baf8d232d4caa5")
    version("2023.03.09", commit="537f6a52a39396f9c05e16a12ab160d8dc8b9d56")
    version("2022.04.26", commit="d28a7a8c9f703075441b700202b8a1ee185ded00")
    version("2023.03.09", commit="537f6a52a39396f9c05e16a12ab160d8dc8b9d56")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("disheng222")

    depends_on("zstd")
    depends_on("gsl")
    depends_on("pkgconfig")
    depends_on("py-pybind11", when="@2023.03.09:")

    def cmake_args(self):
        args = ["-DQoZ_USE_BUNDLED_ZSTD=OFF", "-DQoZ_DEBUG_TIMINGS=OFF"]
        return args
