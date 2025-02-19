# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FluidnumericsSelf(CMakePackage):
    """Spectral Element Library in Fortran."""

    homepage = "https://self.fluidnumerics.com"
    url = "https://github.com/FluidNumerics/SELF/archive/refs/tags/v0.0.1.tar.gz"

    maintainers("fluidnumerics_joe", "garrettbyrd")

    license("BSD-3-Clause-Attribution", checked_by="fluidnumerics_joe")

    version("0.0.1", sha256="c3d4ab7d12f18b9d5864c5f9d7a91c86ebc3b7ff0fec4fa56b5c34b325344259")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "Coverage", "Profile"),
    )
    variant(
        "fp64", default=True, description="Enables double precision floating point arithmetic."
    )
    variant(
        "multithreading",
        default=False,
        description="Enables multithreading of do concurrent loops",
    )
    variant(
        "nthreads",
        default="4",
        description="Sets the number of threads for do concurrent loops",
        values=("2", "4", "6", "8"),
        multi=False,
    )
    variant("examples", default=True, description="Enables build and installation of examples")
    variant("tests", default=False, description="Enables build and installation of unit tests")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("ninja", type="build")
    depends_on("hdf5+fortran+mpi@1.14:")
    depends_on("feq-parse@2.2.2:")
    depends_on("mpi")

    generator("ninja")

    def cmake_args(self):
        args = [
            self.define_from_variant("SELF_ENABLE_EXAMPLES", "examples"),
            self.define_from_variant("SELF_ENABLE_TESTING", "tests"),
            self.define_from_variant("SELF_ENABLE_DOUBLE_PRECISION", "fp64"),
            self.define_from_variant("SELF_ENABLE_MULTITHREADING", "multithreading"),
            self.define_from_variant("SELF_MULTITHREADING_NTHREADS", "nthreads"),
        ]

        return args
