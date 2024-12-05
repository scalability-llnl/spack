# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class ArpackNg(CMakePackage, AutotoolsPackage):
    """ARPACK-NG is a collection of Fortran77 subroutines designed to solve
    large scale eigenvalue problems.

    Important Features:

    * Reverse Communication Interface.
    * Single and Double Precision Real Arithmetic Versions for Symmetric,
      Non-symmetric, Standard or Generalized Problems.
    * Single and Double Precision Complex Arithmetic Versions for Standard or
      Generalized Problems.
    * Routines for Banded Matrices - Standard or Generalized Problems.
    * Routines for The Singular Value Decomposition.
    * Example driver routines that may be used as templates to implement
      numerous Shift-Invert strategies for all problem types, data types and
      precision.

    This project is a joint project between Debian, Octave and Scilab in order
    to provide a common and maintained version of arpack.

    Indeed, no single release has been published by Rice university for the
    last few years and since many software (Octave, Scilab, R, Matlab...)
    forked it and implemented their own modifications, arpack-ng aims to tackle
    this by providing a common repository and maintained versions.

    arpack-ng is replacing arpack almost everywhere.
    """

    homepage = "https://github.com/opencollab/arpack-ng"
    url = "https://github.com/opencollab/arpack-ng/archive/3.3.0.tar.gz"
    git = "https://github.com/opencollab/arpack-ng.git"

    build_system("cmake", "autotools", default="cmake")

    version("develop", branch="master")
    version("3.9.0", sha256="24f2a2b259992d3c797d80f626878aa8e2ed5009d549dad57854bbcfb95e1ed0")
    version("3.8.0", sha256="ada5aeb3878874383307239c9235b716a8a170c6d096a6625bfd529844df003d")
    version("3.7.0", sha256="972e3fc3cd0b9d6b5a737c9bf6fd07515c0d6549319d4ffb06970e64fa3cc2d6")
    version("3.6.3", sha256="64f3551e5a2f8497399d82af3076b6a33bf1bc95fc46bbcabe66442db366f453")
    version("3.6.2", sha256="673c8202de996fd3127350725eb1818e534db4e79de56d5dcee8c00768db599a")
    version("3.6.0", sha256="3c88e74cc10bba81dc2c72c4f5fff38a800beebaa0b4c64d321c28c9203b37ea")
    version("3.5.0", sha256="50f7a3e3aec2e08e732a487919262238f8504c3ef927246ec3495617dde81239")
    version("3.4.0", sha256="69e9fa08bacb2475e636da05a6c222b17c67f1ebeab3793762062248dd9d842f")
    version(
        "3.3.0",
        sha256="ad59811e7d79d50b8ba19fd908f92a3683d883597b2c7759fdcc38f6311fe5b3",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="Activates MPI support")
    variant("icb", default=False, when="@3.6:", description="Activates iso_c_binding support")

    # The function pdlamch10 does not set the return variable.
    # This is fixed upstream
    # see https://github.com/opencollab/arpack-ng/issues/34
    patch("pdlamch10.patch", when="@3.3.0")

    patch("make_install.patch", when="@3.4.0")
    patch("parpack_cmake.patch", when="@3.4.0")

    # Fujitsu compiler does not support 'isnan' function.
    # isnan: function that determines whether it is NaN.
    patch("incompatible_isnan_fix.patch", when="%fj")
    patch("incompatible_isnan_fix.patch", when="@3.7.0%xl")
    patch("incompatible_isnan_fix.patch", when="@3.7.0%xl_r")

    patch("xlf.patch", when="@3.7.0%xl", level=0)
    patch("xlf.patch", when="@3.7.0%xl_r", level=0)

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")

    with when("build_system=autotools"):
        depends_on("automake", type="build")
        depends_on("autoconf", type="build")
        depends_on("libtool@2.4.2:", type="build")
        depends_on("pkgconfig", type="build")

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cflags":
            if spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")

        if name == "fflags":
            if self.spec.satisfies("%cce"):
                flags.append("-hnopattern")

        return (flags, None, None)

    @property
    def libs(self):
        # TODO: do we need spec['arpack-ng:parallel'].libs ?
        # query_parameters = self.spec.last_query.extra_parameters
        libraries = ["libarpack"]

        if self.spec.satisfies("+mpi"):
            libraries = ["libparpack"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        lapack_libs = spec["lapack"].libs.joined(";")
        blas_libs = spec["blas"].libs.joined(";")

        options = [
            self.define("EXAMPLES", "ON"),
            self.define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib),
            self.define("LAPACK_FOUND", True),
            self.define("LAPACK_INCLUDE_DIRS", spec["lapack"].prefix.include),
            self.define("LAPACK_LIBRARIES", lapack_libs),
            self.define("BLAS_FOUND", True),
            self.define("BLAS_INCLUDE_DIRS", spec["blas"].prefix.include),
            self.define("BLAS_LIBRARIES", blas_libs),
            self.define_from_variant("MPI", "mpi"),
            self.define_from_variant("ICB", "icb"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]

        # If 64-bit BLAS is used:
        if (
            spec.satisfies("^openblas+ilp64")
            or spec.satisfies("^intel-mkl+ilp64")
            or spec.satisfies("^intel-parallel-studio+mkl+ilp64")
        ):
            options.append("-DINTERFACE64=1")

        return options


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec
        options = (
            self.enable_or_disable("mpi")
            + [
                f"--with-blas={spec['blas'].libs.ld_flags}",
                f"--with-lapack={spec['lapack'].libs.ld_flags}",
            ]
            + self.enable_or_disable("shared")
        )

        if spec.satisfies("+mpi"):
            options.append(f"F77={spec['mpi'].mpif77}")

        return options

    @when("@:3.7.0 %gcc@10:")
    def setup_build_environment(self, env):
        # version up to and including 3.7.0 are not ported to gcc 10
        # https://github.com/opencollab/arpack-ng/issues/242
        env.set("FFLAGS", "-fallow-argument-mismatch")
