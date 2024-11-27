# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcint(CMakePackage):
    """Library for analytical Gaussian integrals for quantum chemistry."""

    homepage = "https://github.com/sunqm/libcint"
    url = "https://github.com/sunqm/libcint/archive/v3.0.4.tar.gz"
    maintainers("mfherbst", "bruneval")

    license("BSD-2-Clause")

    #
    # Versions
    #
    version("6.1.2", sha256="8287e1eaf2b8c8e19eb7a8ea92fd73898f0884023c503b84624610400adb25c4")
    version("5.5.0", sha256="c822a9a454587d935287de0f64a2c2cf5338323a554a3f34bcfb4a2892daf477")
    version("5.3.0", sha256="9d4fae074b53a8ce0335e2672d423deca2bda6df8020352e59d23c17a0c1239d")
    version("5.2.0", sha256="f9dba1040c445ee81ae5a2a59d9f1291fc0406edad0fb5ea37fceb66c2ef7799")
    version("5.1.3", sha256="a239275a0464360c904fd06e67d2e76ef1147e04bc634befb40c67d3e79b3638")
    version("3.0.13", sha256="ee64f0bc7fb6073063ac3c9bbef8951feada141e197b1a5cc389c8cccf8dc360")
    version("3.0.12", sha256="7409ef41f1465cf4c1ae9834dfc0b0585c0fdc63b55d8ee8b8a7a6d5e31f309d")
    version("3.0.11", sha256="4c9c24d4bd4791391848f19a4be5177137aca27a8e0375574101a7a1261157cf")
    version("3.0.10", sha256="aac6d9630dc4c62840f03262166e877d3aeaf27b6b33498fb490fa3428f12fe4")
    version("3.0.8", sha256="ca94772f74aaf7b8ad4d7c1b09578c9115ec909c3d8b82dacc908c351c631c35")
    version("3.0.7", sha256="e603cd90567c6116d4f704ea66a010b447c11052e90db1d91488adc187142ead")
    version("3.0.6", sha256="a7d6d46de9be044409270b27727a1d620d21b5fda6aa7291548938e1ced25404")
    version("3.0.5", sha256="7bde241ce83c00b89c80459e3af5734d40925d8fd9fcaaa7245f61b08192c722")
    version("3.0.4", sha256="0f25ef7ad282dd7a20e4decf283558e4f949243a5423ff4c0cd875276c310c47")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    #
    # Variants
    #
    variant("f12", default=True, description="Enable explicitly correlated f12 integrals.")
    variant(
        "coulomb_erf", default=True, description="Enable attenuated coulomb operator integrals."
    )
    variant(
        "pypzpx",
        default=False,
        description="Enforce PYPZPX ordering of p-orbitals " "instead of PXPYPZ.",
    )
    variant("test", default=False, description="Build test programs")
    variant("shared", default=True, description="Build the shared library")

    #
    # Dependencies and conflicts
    #
    depends_on("cmake@2.6:", type="build")
    depends_on("blas")
    depends_on("python", type=("build", "test"), when="+test")
    depends_on("py-numpy", type=("build", "test"), when="+test")

    # Libcint tests only work with a shared libcint library
    conflicts("+test~shared")

    #
    # Settings and cmake cache
    #
    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_RANGE_COULOMB=" + str(spec.satisfies("+coulomb_erf")),
            "-DPYPZPX=" + str(spec.satisfies("+pypzpx")),
            "-DWITH_F12=" + str(spec.satisfies("+f12")),
            "-DBUILD_SHARED_LIBS=" + str(spec.satisfies("+shared")),
            "-DENABLE_TEST=" + str(spec.satisfies("+test")),
            "-DENABLE_EXAMPLE=OFF",  # Requires fortran compiler
        ]
        return args
