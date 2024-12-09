# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Compadre(CMakePackage):
    """The Compadre Toolkit provides a performance portable solution for the
    parallel evaluation of computationally dense kernels. The toolkit
    specifically targets the Generalized Moving Least Squares (GMLS) approach,
    which requires the inversion of small dense matrices. The result is a set
    of weights that provide the information needed for remap or entries that
    constitute the rows of some globally sparse matrix.
    """

    homepage = "https://github.com/sandialabs/compadre"
    git = "https://github.com/sandialabs/compadre.git"
    url = "https://github.com/sandialabs/compadre/archive/v1.3.0.tar.gz"
    maintainers("kuberry")

    version("master", branch="master")
    version("1.5.0", sha256="b7dd6020cc5a7969de817d5c7f6c5acceaad0f08dcfd3d7cacfa9f42e4c8b335")
    version("1.4.1", sha256="2e1e7d8e30953f76b6dc3a4c86ec8103d4b29447194cb5d5abb74b8e4099bdd9")
    version("1.3.0", sha256="f711a840fd921e84660451ded408023ec3bcfc98fd0a7dc4a299bfae6ab489c2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("kokkos-kernels@3.3.01:4")
    depends_on("cmake@3.13:", type="build")

    variant("mpi", default=False, description="Enable MPI support")
    depends_on("mpi", when="+mpi")

    variant("tests", default=True, description="Enable tests and examples")

    # fixes duplicate symbol issue with static library build
    patch(
        "https://patch-diff.githubusercontent.com/raw/sandialabs/Compadre/pull/286.patch?full_index=1",
        sha256="e267b74f8ecb8dd23970848ed919d29b7d442f619ce80983e02a19f1d9582c61",
        when="@1.5.0",
    )

    def cmake_args(self):
        spec = self.spec

        kokkos = spec["kokkos"]
        kokkos_kernels = spec["kokkos-kernels"]

        options = []
        options.extend(
            [
                "-DKokkosCore_PREFIX={0}".format(kokkos.prefix),
                "-DKokkosKernels_PREFIX={0}".format(kokkos_kernels.prefix),
                "-DCMAKE_CXX_COMPILER:STRING={0}".format(spec["kokkos"].kokkos_cxx),
            ]
        )

        if spec.satisfies("+mpi"):
            options.append("-DCompadre_USE_MPI:BOOL=ON")

        if spec.satisfies("~tests"):
            options.append("-DCompadre_EXAMPLES:BOOL=OFF")
            options.append("-DCompadre_TESTS:BOOL=OFF")

        if spec.satisfies("+shared"):
            options.append("-DBUILD_SHARED_LIBS:BOOL=ON")
        else:
            options.append("-DBUILD_SHARED_LIBS:BOOL=OFF")

        return options
