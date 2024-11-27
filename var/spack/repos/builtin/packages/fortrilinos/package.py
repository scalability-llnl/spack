# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fortrilinos(CMakePackage):
    """ForTrilinos provides a set of Fortran-2003 wrappers to the Trilinos
    solver library.

    Note that most properties are *transitive* from the underlying Trilinos
    configuration. For example, MPI is enabled if and only if the linked
    Trilinos version has it, so this package does not provide an indepdent
    variant. Instead, use ``fortrilinos ^trilinos~mpi`` to disable MPI support.
    """

    homepage = "https://trilinos.github.io/ForTrilinos/"
    url = (
        "https://github.com/trilinos/ForTrilinos/releases/download/v2.1.0/ForTrilinos-2.1.0.tar.gz"
    )
    git = "https://github.com/trilinos/ForTrilinos.git"

    maintainers("sethrj", "aprokop")

    tags = ["e4s"]
    test_requires_compiler = True

    license("BSD-3-Clause")

    version("2.3.0", sha256="7be5efecaea61ad773d3fe182aa28735ebc3e7af821e1805ad284e4ed4e31a49")
    version("2.2.0", sha256="9e73fc71066bfaf7cde040e1467baf7a1ec797ff2874add49f9741e93f9fffb5")
    version("2.1.0", sha256="2c62bb6106ae86a804497d549080cb6877c5d860b6bf2e72ec5cbcbbe63e3b5b")
    version("2.0.1", sha256="291a62c885cd4ffd76cbebafa02789649bd4fa73f1005cf8da51fd153acb9e1a")
    version("2.0.0", sha256="4382a21864e70e9059654c0529cac95548768fe02855c5f3624e454807dff018")

    # Note: spack version comparison implies Version('2.0.0') <
    # Version('2.0.0-dev1'), so this is the best workaround I could find.
    version(
        "2.0.dev3",
        sha256="c20a34b374a56b050bc1db0be1d3db63fca3e59c5803af0cb851b044ac84e6b3",
        url="https://github.com/trilinos/ForTrilinos/archive/v2.0.0-dev3.tar.gz",
    )
    version(
        "2.0.dev2",
        sha256="2a55c668b3fe986583658d272eab2dc076b291a5f2eb582a02602db86a32030b",
        url="https://github.com/trilinos/ForTrilinos/archive/v2.0.0-dev2.tar.gz",
    )
    version("master", branch="master")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hl", default=True, description="Build high-level Trilinos wrappers")
    variant("shared", default=True, description="Build shared libraries")

    # Trilinos version dependencies
    depends_on("trilinos@14.0", when="@2.3")
    depends_on("trilinos@13.4", when="@2.2")
    depends_on("trilinos@13.2", when="@2.1.0:2.1")
    depends_on("trilinos@13:13.2", when="@2.0")
    depends_on("trilinos@12.18.1", when="@2.0.dev3")
    depends_on("trilinos@12.18.1", when="@2.0.dev2")

    # Baseline trilinos dependencies
    depends_on("trilinos gotype=long_long")
    # Full trilinos dependencies
    depends_on(
        "trilinos+amesos2+anasazi+belos+kokkos+ifpack2+muelu+nox+tpetra" "+stratimikos", when="+hl"
    )

    @run_before("cmake")
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies, require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError("ForTrilinos requires a Fortran compiler")

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("ForTrilinos_EXAMPLES", self.run_tests),
            self.define("ForTrilinos_TESTING", self.run_tests),
        ]

    examples_src_dir = "example/test-installation"

    @property
    def cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

    @run_after("install")
    def setup_smoke_tests(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.examples_src_dir])

    def test_installation(self):
        """build and run ctest against the installed software"""
        cmake_args = [
            self.define("CMAKE_PREFIX_PATH", self.prefix),
            self.define("CMAKE_CXX_COMPILER", self.compiler.cxx),
            self.define("CMAKE_Fortran_COMPILER", self.compiler.fc),
            self.cached_tests_work_dir,
        ]
        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        ctest = which("ctest")
        make = which("make")

        with working_dir(self.cached_tests_work_dir, create=True):
            cmake(*cmake_args)
            make()
            out = ctest("-V", output=str.split, error=str.split)
            assert "100% tests passed" in out
