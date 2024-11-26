# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    homepage = "https://github.com/SNLComputation/compadre"
    git = "https://github.com/SNLComputation/compadre.git"
    url = "https://github.com/SNLComputation/compadre/archive/v1.3.0.tar.gz"
    maintainers("kuberry")

    version("master", branch="master", preferred=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("trilinos", default=False, description="Use Kokkos from Trilinos")
    variant(
        "debug",
        default="0",
        values=["0", "1", "2"],
        multi=False,
        description="Debugging level 0) release 1) debug 2) extreme debugging",
    )

    depends_on("cmake@3.10.0:", type="build")
    depends_on("python@3.4:", type=("build", "link", "run"))
    depends_on("py-pip", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.23:", type="build")
    depends_on("trilinos@13.2:", when="+trilinos")

    @run_before("install")
    def set_cmake_from_variants(self):
        spec = self.spec
        with open("cmake_opts.txt", "w") as f:
            if "+trilinos" in spec:
                f.write("Trilinos_PREFIX:PATH=%s\n" % spec["trilinos"].prefix)
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
