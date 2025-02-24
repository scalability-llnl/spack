# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mpidiff(CMakePackage):
    """Library for comparing numerical differences between binaries."""

    homepage = "https://github.com/LLNL/MPIDiff"
    url = "https://github.com/LLNL/MPIDiff/archive/refs/tags/v0.2.0.tar.gz"

    maintainers("adayton1")

    license("BSD-3-Clause", checked_by="alecbcs")

    version("0.2.0", sha256="726b59fe4af0bb0812fc34c456cb0d801e03313a8fdfb9dc63d23a9b316b6118")

    variant("docs", default=False, description="Build and include documentation")
    variant("examples", default=False, description="Build and include examples")
    variant("tests", default=False, description="Build tests")

    depends_on("cxx", type="build")

    depends_on("blt", type="build")
    depends_on("mpi")

    def cmake_args(self):
        spec = self.spec
        return [
            self.define("MPI_DIR", spec["mpi"].prefix),
            self.define("BLT_SOURCE_DIR", spec["blt"].prefix),
            self.define_from_variant("MPIDIFF_ENABLE_DOCS", "docs"),
            self.define_from_variant("MPIDIFF_ENABLE_EXAMPLES", "examples"),
            self.define_from_variant("MPIDIFF_ENABLE_TESTS", "tests"),
        ]
