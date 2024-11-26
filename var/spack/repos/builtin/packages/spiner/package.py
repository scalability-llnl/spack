# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spiner(CMakePackage, CudaPackage):
    """Spiner:
    Performance portable routines for generic, tabulated, multi-dimensional data"""

    homepage = "https://github.com/lanl/spiner"
    url = "https://github.com/lanl/spiner/archive/refs/tags/1.4.0.tar.gz"
    git = "https://github.com/lanl/spiner.git"

    maintainers("rbberger")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("1.6.2", sha256="91fb403ce3b151fbdf8b6ff5aed0d8dde1177749f5633951027b100ebc7080d3")
    version("1.6.1", sha256="52774322571d3b9b0dc3c6b255257de9af0e8e6170834360f2252c1ac272cbe7")
    version("1.6.0", sha256="afa5526d87c78c1165ead06c09c5c2b9e4a913687443e5adff7b709ea4dd7edf")
    version(
        "1.5.1",
        sha256="dd1cada84446443e8925438b8da53ab5a6cb9f373f1a993905ef0bf51f48223c",
        deprecated=True,
    )
    version(
        "1.5.0",
        sha256="b27ddabc0d21870b845444c24307d3a0c1b175483e72cc138139d6e0dd29b244",
        deprecated=True,
    )
    version(
        "1.4.0",
        sha256="c3801b9eab26feabec33ff8c59e4056f384287f407d23faba010d354766f3ac5",
        deprecated=True,
    )

    depends_on("c", type="build")  # todo: disable cmake default?
    depends_on("cxx", type="build")

    # When overriding/overloading varaints, the last variant is always used, except for
    # "when" clauses. Therefore, call the whens FIRST then the non-whens.
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#overriding-variants
    variant("kokkos", default=False, description="Enable kokkos")
    variant("openmp", default=False, description="Enable openmp kokkos backend")

    variant("hdf5", default=False, description="Enable hdf5")
    variant("mpi", default=False, description="Support parallel hdf5")

    variant("python", default=False, description="Python, Numpy & Matplotlib Support")

    depends_on("cmake@3.12:", when="@:1.5.1", type="build")
    depends_on("cmake@3.23:", when="@1.6.0:", type="build")
    depends_on("catch2@2.13.4:2.13.9", type="test")
    depends_on("ports-of-call@1.2.0:", when="@:1.5.1")
    depends_on("ports-of-call@1.5.1:", when="@1.6.0:")
    depends_on("ports-of-call@main", when="@main")

    # Currently the raw cuda backend of ports-of-call is not supported.
    depends_on("ports-of-call portability_strategy=Kokkos", when="@:1.5.1 +kokkos")
    depends_on("ports-of-call portability_strategy=None", when="@:1.5.1 ~kokkos")
    for _flag in list(CudaPackage.cuda_arch_values):
        depends_on("kokkos@3.3.00: cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)
    for _flag in ("~cuda", "+cuda", "~openmp", "+openmp"):
        depends_on("kokkos@3.3.00: " + _flag, when="+kokkos" + _flag)
    depends_on("kokkos@3.3.00: ~shared+wrapper+cuda_lambda+cuda_constexpr", when="+cuda+kokkos")

    depends_on("hdf5+hl~mpi", when="+hdf5~mpi")
    depends_on("hdf5+hl+mpi", when="+hdf5+mpi")

    depends_on("python", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-matplotlib", when="+python")

    conflicts("+mpi", when="~hdf5")
    conflicts("+cuda", when="~kokkos")
    conflicts("+openmp", when="~kokkos")
    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")

    def cmake_args(self):
        if self.spec.satisfies("@1.6.0:"):
            use_kokkos_option = "SPINER_TEST_USE_KOKKOS"
            use_cuda_option = "SPINER_TEST_USE_CUDA"
        else:
            use_kokkos_option = "SPINER_USE_KOKKOS"
            use_cuda_option = "SPINER_USE_CUDA"

        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant(use_kokkos_option, "kokkos"),
            self.define_from_variant(use_cuda_option, "cuda"),
            self.define_from_variant("SPINER_USE_HDF", "hdf5"),
        ]
        if "+cuda" in self.spec:
            args.append(
                self.define("CMAKE_CUDA_ARCHITECTURES", self.spec.variants["cuda_arch"].value)
            )
        return args
