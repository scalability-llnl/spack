# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycompadre(PythonPackage):
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
    version("1.6.0", sha256="5d937f85c2e64b50955beab1ac9f1083162f5239a5f13a40ef9a9c0e6ad216c9")
    version("1.5.0", sha256="b7dd6020cc5a7969de817d5c7f6c5acceaad0f08dcfd3d7cacfa9f42e4c8b335")
    version("1.4.1", sha256="2e1e7d8e30953f76b6dc3a4c86ec8103d4b29447194cb5d5abb74b8e4099bdd9")
    version("1.3.0", sha256="f711a840fd921e84660451ded408023ec3bcfc98fd0a7dc4a299bfae6ab489c2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "debug",
        default="0",
        values=["0", "1", "2"],
        multi=False,
        description="Debugging level 0) release 1) debug 2) extreme debugging",
    )

    depends_on("cmake@3.10:", type="build", when="@:1.4")
    depends_on("cmake@3.16:", type="build", when="@1.5:")

    depends_on("kokkos-kernels@3.3.01:4", when="@:1.5")
    depends_on("kokkos-kernels@4:", when="@1.6:")

    depends_on("python@3.4:", type=("build", "link", "run"), when="@:1.5")
    depends_on("python@3.6:", type=("build", "link", "run"), when="@1.6:")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.23:", type="build")

    # fixes duplicate symbol issue with static library build
    patch(
        "https://patch-diff.githubusercontent.com/raw/sandialabs/Compadre/pull/286.patch?full_index=1",
        sha256="e267b74f8ecb8dd23970848ed919d29b7d442f619ce80983e02a19f1d9582c61",
        when="@1.5.0",
    )

    @run_before("install")
    def set_cmake_from_variants(self):
        spec = self.spec
        with open("cmake_opts.txt", "w") as f:
            f.write("KokkosCore_PREFIX:PATH=%s\n" % spec["kokkos"].prefix)
            f.write("KokkosKernels_PREFIX:PATH=%s\n" % spec["kokkos-kernels"].prefix)
            f.write("CMAKE_CXX_COMPILER:STRING={0}\n".format(spec["kokkos"].kokkos_cxx))
            if spec.variants["debug"].value == "0":
                f.write(
                    "CMAKE_CXX_FLAGS:STRING=%s\n"
                    % "' -Ofast -funroll-loops -march=native -mtune=native '"
                )
                f.write("Compadre_DEBUG:BOOL=OFF\n")
            else:
                f.write("CMAKE_CXX_FLAGS:STRING=%s\n" % "'-g -O0'")
                f.write("CMAKE_BUILD_TYPE:STRING=%s\n" % "DEBUG")
                f.write("Compadre_DEBUG:BOOL=ON\n")
                if spec.variants["debug"].value == "2":
                    f.write("Compadre_EXTREME_DEBUG:BOOL=ON\n")
