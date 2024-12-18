# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Dftfe(CMakePackage):
    """Real-space DFT calculations using Finite Elements"""

    homepage = "https://sites.google.com/umich.edu/dftfe/"
    url = "https://github.com/dftfeDevelopers/dftfe/archive/0.5.1.tar.gz"

    maintainers("rmsds")

    license("LGPL-2.1-or-later")

    version("0.6.0", sha256="66b633a3aae2f557f241ee45b2faa41aa179e4a0bdf39c4ae2e679a2970845a1")
    version("0.5.2", sha256="9dc4fa9f16b00be6fb1890d8af4a1cd3e4a2f06a2539df999671a09f3d26ec64")
    version("0.5.1", sha256="e47272d3783cf675dcd8bc31da07765695164110bfebbbab29f5815531f148c1")
    version("0.5.0", sha256="9aadb9a9b059f98f88c7756b417423dc67d02f1cdd2ed7472ba395fcfafc6dcb")

    depends_on("cxx", type="build")  # generated

    variant(
        "scalapack",
        default=True,
        description="Use ScaLAPACK, strongly recommended for problem sizes >5000 electrons",
    )
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    depends_on("mpi")
    depends_on("dealii+p4est+petsc+slepc+int64+scalapack+mpi")
    depends_on("dealii+p4est+petsc+slepc+int64+scalapack+mpi@9.0.0:", when="@0.5.1:")
    depends_on("scalapack", when="+scalapack")
    depends_on("alglib")
    depends_on("libxc")
    depends_on("spglib")
    depends_on("libxml2")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DCMAKE_C_COMPILER={0}".format(spec["mpi"].mpicc),
            "-DCMAKE_CXX_COMPILER={0}".format(spec["mpi"].mpicxx),
            "-DALGLIB_DIR={0}".format(spec["alglib"].prefix),
            "-DLIBXC_DIR={0}".format(spec["libxc"].prefix),
            "-DXML_LIB_DIR={0}/lib".format(spec["libxml2"].prefix),
            "-DXML_INCLUDE_DIR={0}/include".format(spec["libxml2"].prefix),
            "-DSPGLIB_DIR={0}".format(spec["spglib"].prefix),
        ]

        if spec.satisfies("^intel-mkl"):
            args.append("-DWITH_INTEL_MKL=ON")
        else:
            args.append("-DWITH_INTEL_MKL=OFF")

        if spec.satisfies("%gcc"):
            args.append("-DCMAKE_C_FLAGS=-fpermissive")
            args.append("-DCMAKE_CXX_FLAGS=-fpermissive")

        return args

    @when("@:0.5.2")
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib64)
        install(join_path(self.build_directory, "main"), join_path(prefix.bin, "dftfe"))
        install(join_path(self.build_directory, "libdftfe.so"), prefix.lib64)
