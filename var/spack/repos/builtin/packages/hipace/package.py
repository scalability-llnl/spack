# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipace(CMakePackage):
    """Highly efficient Plasma Accelerator Emulation, quasistatic
    particle-in-cell code
    """

    homepage = "https://hipace.readthedocs.io"
    url = "https://github.com/Hi-PACE/hipace/archive/refs/tags/v23.07.tar.gz"
    git = "https://github.com/Hi-PACE/hipace.git"

    maintainers("ax3l", "MaxThevenet", "SeverinDiederichs")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="development")
    version("23.07", sha256="2b1f61c91d2543d7ee360eba3630c864107e29f7bcfd0221451beea88f414f21")
    version("23.05", sha256="33a15cfeada3ca16c2a3af1538caa7ff731df13b48b884045a0fe7974382fcd1")
    version("21.09", sha256="5d27824fe6aac47ce26ca69759140ab4d7844f9042e436c343c03ea4852825f1")

    depends_on("cxx", type="build")  # generated

    variant(
        "compute",
        default="noacc",
        values=("omp", "cuda", "hip", "sycl", "noacc"),
        multi=False,
        description="On-node, accelerated computing backend",
    )
    variant("mpi", default=True, description="Enable MPI support")
    variant("openpmd", default=True, description="Enable openPMD I/O")
    variant(
        "precision",
        default="double",
        values=("single", "double"),
        multi=False,
        description="Floating point precision (single/double)",
    )

    depends_on("cmake@3.18.0:", type="build", when="@23.05:")
    depends_on("cmake@3.15.0:", type="build")
    depends_on("mpi", when="+mpi")
    with when("+openpmd"):
        depends_on("openpmd-api@0.15.1:", when="@23.05:")
        depends_on("openpmd-api@0.14.2:")
        depends_on("openpmd-api ~mpi", when="~mpi")
        depends_on("openpmd-api +mpi", when="+mpi")
    with when("compute=noacc"):
        depends_on("fftw@3: ~mpi", when="~mpi")
        depends_on("fftw@3: +mpi", when="+mpi")
        depends_on("pkgconfig", type="build")
    with when("compute=omp"):
        depends_on("fftw@3: +openmp")
        depends_on("fftw ~mpi", when="~mpi")
        depends_on("fftw +mpi", when="+mpi")
        depends_on("pkgconfig", type="build")
        depends_on("llvm-openmp", when="%apple-clang")
    with when("compute=cuda"):
        depends_on("cuda@:12.1", when="%gcc@:12.2")
        depends_on("cuda@:12.0", when="%gcc@:12.1")
        depends_on("cuda@:12.1", when="%gcc@:12.2")
        depends_on("cuda@:11.8", when="%gcc@:9")
        depends_on("cuda@:10", when="%gcc@:8")
        depends_on("cuda@9.2.88:")
    with when("compute=hip"):
        depends_on("rocfft")
        depends_on("rocprim")
        depends_on("rocrand")

    def cmake_args(self):
        spec = self.spec

        args = [
            # do not super-build dependencies
            "-HiPACE_openpmd_internal=OFF",
            # variants
            "-DHiPACE_COMPUTE={0}".format(spec.variants["compute"].value.upper()),
            self.define_from_variant("HiPACE_MPI", "mpi"),
            self.define_from_variant("HiPACE_OPENPMD", "openpmd"),
            "-DHiPACE_PRECISION={0}".format(spec.variants["precision"].value.upper()),
        ]

        return args
