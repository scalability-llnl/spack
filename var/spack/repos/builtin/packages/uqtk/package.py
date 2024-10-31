# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Uqtk(CMakePackage):
    """Sandia Uncertainty Quantification Toolkit. The UQ Toolkit (UQTk) is a
    collection of libraries and tools for the quantification of uncertainty
    in numerical model predictions"""

    homepage = "https://www.sandia.gov/UQToolkit/"
    url = "https://github.com/sandialabs/UQTk/archive/v3.0.4.tar.gz"
    git = "https://github.com/sandialabs/UQTk.git"

    maintainers("omsai", "bjdebus")

    version("master", branch="master")
    version("3.1.3", sha256="37840630357c4f407191d7a4276dfe219df35d54d288d68fea1746dfcbc3c5c1")
    version("3.1.2", sha256="57ce0cea709777cbefb46f3bd86a0996a0ed5f50fc54cc297599df6e4bb9ab83")
    version("3.1.0", sha256="56ecd3d13bdd908d568e9560dc52cc0f66d7bdcdbe64ab2dd0147a7cf1734f97")
    version("3.0.4", sha256="0a72856438134bb571fd328d1d30ce3d0d7aead32eda9b7fb6e436a27d546d2e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "python", default=True, description="Compile Python scripts and interface to C++ libraries"
    )

    depends_on("expat")
    depends_on("sundials@6:", when="@3.1.3:")
    depends_on("sundials@:5", when="@3.1.0:3.1.2")
    depends_on("blas", when="@3.1.0:")
    depends_on("lapack", when="@3.1.0:")

    extends("python", when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-scipy", type=("build", "run"), when="+python")
    depends_on("py-matplotlib", type=("build", "run"), when="+python")
    depends_on("py-pymc3", type=("build", "run"), when="+python")
    depends_on("swig", type="build", when="@:3.1.0 +python")

    # The two patches for 3.1.0 fail with 3.1.2, therefore convert the patches
    # to more versatile and reliable sed-like filter_file substitutions.
    def patch(self):
        # These patches affect many CMakeLists.txt files.
        cmakelists = find(".", "CMakeLists.txt")

        # All patched lines start with "target_link_libraries";
        # case-insensitive.
        tll = (
            r"(.*[tT][aA][rR][gG][eE][tT]_[lL][iI][nN][kK]_"
            r"[lL][iI][bB][rR][aA][rR][iI][eE][sS].+)"
        )

        # Modify the process of directly specifying blas/lapack as the library
        # name.
        if "@3.1.0:3.1.2" in self.spec:
            lp = r"\${LAPACK_LIBRARIES}"
            bl = r"\${BLAS_LIBRARIES}"
            # Replace duplicate entries.
            filter_file(rf"{tll}lapack ({lp}.+)", r"\1 \2", *cmakelists)
            filter_file(rf"{tll}blas ({lp}.+)", r"\1 \2", *cmakelists)
            # Replace with the variable.
            filter_file(rf"{tll}lapack(.+)", rf"\1{lp}\2", *cmakelists)
            filter_file(rf"{tll}blas(.+)", rf"\1{bl}\2", *cmakelists)

        # Do not link the gfortran library for the Fujitsu compiler.
        if "@3.1.0:%fj" in self.spec:
            filter_file(rf"{tll} gfortran(.+stdc[+][+].+)", r"\1\2", *cmakelists)

    @when("@3.1.0:")
    def cmake_args(self):
        spec = self.spec

        # Make sure we use Spack's blas/lapack:
        lapack_libs = spec["lapack"].libs.joined(";")
        blas_libs = spec["blas"].libs.joined(";")

        args = [
            self.define("CMAKE_SUNDIALS_DIR", spec["sundials"].prefix),
            self.define("LAPACK_LIBRARIES", lapack_libs),
            self.define("BLAS_LIBRARIES", blas_libs),
            self.define_from_variant("PyUQTk", "python"),
        ]

        return args

    def setup_run_environment(self, env):
        if "+python" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix)
            env.prepend_path("PYTHONPATH", "{0}/PyUQTk".format(self.prefix))
            env.prepend_path("LD_LIBRARY_PATH", "{0}/PyUQTk/".format(self.prefix))
            env.set("UQTK_SRC", self.prefix)
            env.set("UQTK_INS", self.prefix)
