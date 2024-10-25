# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dftbplus(CMakePackage, MakefilePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    url = "https://github.com/dftbplus/dftbplus/releases/download/22.1/dftbplus-22.1.tar.xz"
    git = "https://github.com/dftbplus/dftbplus.git"

    maintainers("HaoZeke", "aradi", "iamashwin99")
    generator("ninja")

    build_system(
        conditional("cmake", when="@20.1:"),
        conditional("makefile", when="@:19.1"),
        default="cmake",
    )

    license("CC-BY-SA-4.0")

    version("main", branch="main")
    version("24.1", sha256="3bc405d1ab834b6b145ca671fb44565ec50a6f576e9e18e7a1ae2c613a311321")
    version("23.1", sha256="e2d0471c2fd3aaf174a9aac44fd8e7de2668d182201779626d6e62754adc4cf9")
    version("22.2", sha256="0140f5f2e24d3071e5e7aede2ed6216a6f46d55216b0d69da17af917c62e98ed")
    version("22.1", sha256="02daca6f4c6372656598f3ba0311110c8e473c87c8d934d7bb276feaa4cc1c82")
    version("21.2", sha256="fbeb0e0ea93ab4dc4450f298ec712d2cf991f19f621badf57dae05f0e43b5906")
    version("21.1", sha256="8c1eb8a38f72c421e2ae20118a6db3a656fa84e8b180ef387e549a73ae77f970")
    version("20.2.1", sha256="95cc85fdb08bd57ca013bd09f4f902303720e17d015a5fab2d4db63fcb6d9cb3")
    version("20.2", sha256="eafd219159d600624041658046c89db539ceb0c1d2988b72321c80d9b992c9bf")
    version("20.1", sha256="04c2b906b8670937c8ddd9c5fb68e7e9921b464840cf54aa3d698db98167d0b7")
    version(
        "19.1",
        deprecated=True,
        sha256="78f45ef0571c78cf732a5493d32830455a832fa05ebcad43098895e46ad8d220",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "api",
        default=True,
        description="Whether public API should be included and the DFTB+ library installed.",
    )
    variant(
        "arpack",
        default=False,
        description="Whether the ARPACK library should be included (needed for TD-DFTB).",
        when="~mpi",
    )
    variant(
        "chimes",
        default=False,
        when="@21.2:",
        description="Whether repulsive corrections" "via the ChIMES library should be enabled.",
    )
    variant(
        "elsi",
        default=False,
        description="Use the ELSI library for large scale systems. "
        "Only has any effect if you build with '+mpi'",
        when="+mpi",
    )
    variant(
        "gpu",
        default=False,
        description="Use the MAGMA library " "for GPU accelerated computation",
    )
    variant(
        "mbd",
        default=False,
        when="@21.1:",
        description="Whether DFTB+ should be built with many-body-dispersion support.",
    )
    variant("mpi", default=False, description="Whether DFTB+ should support MPI-parallelism.")
    variant(
        "openmp",
        default=True,
        description="Whether OpenMP thread parallisation should be enabled.",
    )
    variant(
        "plumed",
        default=False,
        when="@20.1:",
        description="Whether metadynamics via the PLUMED2 library should be allowed.",
    )
    variant("poisson", default=False, description="Whether the Poisson-solver should be included.")
    variant(
        "python",
        default=False,
        description="Whether the Python components of DFTB+ should be tested and installed.",
    )
    variant(
        "sdftd3",
        default=False,
        when="@21.2:",
        description="Whether the s-dftd3 library should be included",
    )
    variant(
        "sockets",
        default=False,
        description="Whether the socket library " "(external control) should be linked",
    )
    variant(
        "transport",
        default=False,
        when="+shared",
        description="Whether transport via libNEGF should be included. "
        "Only affects parallel build. "
        "(serial version is built without libNEGF/transport)",
    )
    variant(
        "tblite",
        default=False,
        when="@21.2:",
        description="Whether xTB support should be included via tblite.",
    )

    variant("shared", default=False, description="Most often for the Python wrappers.")

    variant(
        "dftd3",
        default=False,
        when="@:19.1",
        description="Use DftD3 dispersion library " "(if you need this dispersion model)",
    )

    depends_on("cmake@3.16:", type="build", when="@20.1:")
    depends_on("ninja@1.10", type="build", when="@20.1:")

    depends_on("blas", when="-mpi")
    depends_on("lapack", when="-mpi")

    depends_on("arpack-ng", when="+arpack~mpi")
    depends_on("simple-dftd3", when="+sdftd3")
    depends_on("elsi", when="+elsi")
    depends_on("magma", when="+gpu")
    depends_on("mpi", when="+mpi")
    depends_on("plumed", when="+plumed")
    depends_on("scalapack", when="+mpi")
    depends_on("python@3.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))  # for tests
    # Only for 19.1
    depends_on("dftd3-lib@0.9.2", when="+dftd3")

    # Conflicts
    conflicts("+python", when="~shared")
    conflicts("-poisson", when="+transport")

    # Extensions
    extends("python", when="+python")

    @when("@19.1")  # Only version without CMake
    def edit(self, spec, prefix):
        """
        First, change the ROOT variable, because, for some reason,
        the Makefile and the spack install script run in different directories
        Then, if using GCC, rename the file 'sys/make.x86_64-linux-gnu'
        to make.arch.
        After that, edit the make.arch to point to the dependencies
        And the last thing we do here is to set the installdir
        """
        dircwd = os.getcwd()
        makefile = FileFilter("makefile")
        makefile.filter("ROOT := .*", "ROOT := {0}".format(dircwd))

        archmake = join_path(".", "sys", "make.x86_64-linux-gnu")
        copy(archmake, join_path(dircwd, "make.arch"))

        march = FileFilter(join_path(dircwd, "make.arch"))

        mconfig = FileFilter(join_path(dircwd, "make.config"))

        mconfig.filter("INSTALLDIR := .*", "INSTALLDIR := {0}".format(prefix))

        if self.spec.satisfies("+gpu"):
            march.filter("MAGMADIR = .*", "MAGMADIR = {0}".format(spec["magma"].prefix))

            mconfig.filter("WITH_GPU := .*", "WITH_GPU := 1")

        if self.spec.satisfies("+mpi"):
            march.filter(
                "SCALAPACKDIR = .*", "SCALAPACKDIR = {0}".format(spec["scalapack"].prefix)
            )

            march.filter(
                "LIB_LAPACK = -l.*", "LIB_LAPACK = {0}".format(spec["blas"].libs.ld_flags)
            )

            march.filter("mpifort", "{0}".format(spec["mpi"].mpifc))

            mconfig.filter("WITH_MPI := .*", "WITH_MPI := 1")

            if self.spec.satisfies("+elsi"):
                mconfig.filter("WITH_ELSI := .*", "WITH_ELSI := 1")

                has_pexsi = "+enable_pexsi" in spec["elsi"]

                mconfig.filter(
                    "WITH_PEXSI := .*",
                    "WITH_PEXSI := {0}".format("1" if has_pexsi is True else "0"),
                )

                march.filter(
                    "ELSIINCDIR .*", "ELSIINCDIR = {0}".format(spec["elsi"].prefix.include)
                )

                march.filter("ELSIDIR .*", "ELSIDIR = {0}".format(spec["elsi"].prefix))

        else:
            march.filter(
                "LIB_LAPACK += -l.*", "LIB_LAPACK += {0}".format(spec["blas"].libs.ld_flags)
            )

        if self.spec.satisfies("+sockets"):
            mconfig.filter("WITH_SOCKETS := .*", "WITH_SOCKETS := 1")

        if self.spec.satisfies("+transport"):
            mconfig.filter("WITH_TRANSPORT := .*", "WITH_TRANSPORT := 1")

        if self.spec.satisfies("+arpack"):
            march.filter(
                "ARPACK_LIBS = .*", "ARPACK_LIBS = {0}".format(spec["arpack-ng"].libs.ld_flags)
            )

            mconfig.filter("WITH_ARPACK := .*", "WITH_ARPACK := 1")

        if self.spec.satisfies("+dftd3"):
            march.filter("COMPILE_DFTD3 = .*", "COMPILE_DFTD3 = 0")
            march.filter(
                "DFTD3_INCS = .*", "DFTD3_INCS = -I{0}".format(spec["dftd3-lib"].prefix.include)
            )

            march.filter(
                "DFTD3_LIBS = .*", "DFTD3_LIBS = -L{0} -ldftd3".format(spec["dftd3-lib"].prefix)
            )

            mconfig.filter("WITH_DFTD3 := .*", "WITH_DFTD3 := 1")

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_OPENMP", "openmp"),
            self.define_from_variant("WITH_API", "api"),
            self.define_from_variant("WITH_ARPACK", "arpack"),
            self.define_from_variant("WITH_CHIMES", "chimes"),
            self.define_from_variant("WITH_ELSI", "elsi"),
            self.define_from_variant("WITH_GPU", "gpu"),
            self.define_from_variant("WITH_MBD", "mbd"),
            self.define_from_variant("WITH_MPI", "mpi"),
            self.define_from_variant("WITH_PLUMED", "plumed"),
            self.define_from_variant("WITH_POISSON", "poisson"),
            self.define_from_variant("WITH_PYTHON", "python"),
            self.define_from_variant("WITH_SDFTD3", "sdftd3"),
            self.define_from_variant("WITH_SOCKETS", "sockets"),
            self.define_from_variant("WITH_TBLITE", "tblite"),
            self.define_from_variant("WITH_TRANSPORT", "transport"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        # SCALAPACK
        # Note: dftbplus@20.1 uses plural form of the option names
        #       (e.g. -DSCALAPACK_LIBRARIES)
        # but dftbplus@20.2 onwards uses singular
        #       (e.g. -DSCALAPACK_LIBRARY)
        # and plural form is ignored.
        # We set both inorder to be compatible with all versions.
        if self.spec.satisfies("+mpi"):
            # we use scalapack for linear algebra
            args.extend(
                [
                    self.define("SCALAPACK_FOUND", "true"),
                    self.define("SCALAPACK_INCLUDE_DIRS", self.spec["scalapack"].prefix.include),
                    self.define("SCALAPACK_LIBRARIES", self.spec["scalapack"].libs.joined(";")),
                    self.define("SCALAPACK_LIBRARY", self.spec["scalapack"].libs.joined(";")),
                ]
            )
        else:
            # we define the lapack and blas libraries
            lapack_libs = self.spec["lapack"].libs.joined(";")
            blas_libs = self.spec["blas"].libs.joined(";")
            args.extend(
                [
                    self.define("LAPACK_FOUND", True),
                    self.define("LAPACK_INCLUDE_DIRS", self.spec["lapack"].prefix.include),
                    self.define("LAPACK_LIBRARIES", lapack_libs),
                    self.define("LAPACK_LIBRARY", lapack_libs),
                    self.define("BLAS_FOUND", True),
                    self.define("BLAS_INCLUDE_DIRS", self.spec["blas"].prefix.include),
                    self.define("BLAS_LIBRARIES", blas_libs),
                    self.define("BLAS_LIBRARY", blas_libs),
                ]
            )
        if self.spec.satisfies("+python"):
            args.append(self.define("BUILD_SHARED_LIBS", True))
        if self.run_tests:
            args.append("-DWITH_UNIT_TESTS=ON")
        else:
            args.append("-DWITH_UNIT_TESTS=OFF")
        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Run ctest after building binary.
        only run the unit tests. If the unit tests fail, the installation throws
        a warning."""

        with working_dir(self.build_directory):
            try:
                ctest("")
            except ProcessError:
                warn = "Unit tests failed.\n"
                warn += "Please report this failure to:\n"
                warn += "https://github.com/dftbplus/dftbplus/issues"
                tty.msg(warn)
