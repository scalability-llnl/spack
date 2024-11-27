# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Formetis(CMakePackage):
    """Automated Fortran bindings to METIS and ParMETIS."""

    homepage = "https://github.com/swig-fortran/formetis"
    url = "https://github.com/swig-fortran/formetis/archive/refs/tags/v0.0.1.tar.gz"

    maintainers("sethrj")

    test_requires_compiler = True

    license("MIT")

    version("0.0.2", sha256="0067c03ca822f4a3955751acb470f21eed489256e2ec5ff24741eb2b638592f1")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Enable ParMETIS support")
    variant("shared", default=True, description="Build shared libraries")
    variant("swig", default=False, description="Regenerate source files using SWIG")

    depends_on("metis@5:")
    depends_on("parmetis", when="+mpi")
    depends_on("mpi", when="+mpi")
    depends_on("swig@4.0.2-fortran", when="+swig")

    # Using non-standard int sizes requires regenerating the C/Fortran
    # interface files with SWIG
    conflicts("~swig", when="^metis+int64")
    conflicts("~swig", when="^metis+real64")

    def cmake_args(self):
        from_variant = self.define_from_variant
        args = [
            from_variant("FORMETIS_USE_MPI", "mpi"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("FORMETIS_USE_SWIG", "swig"),
            self.define("FORMETIS_BUILD_EXAMPLES", False),
        ]
        return args

    examples_src_dir = "example"

    @run_after("install")
    def setup_smoke_tests(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.examples_src_dir])

    @property
    def cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

    def test_metis(self):
        """build and run metis"""
        cmake_args = [
            self.define("CMAKE_PREFIX_PATH", self.prefix),
            self.define("CMAKE_Fortran_COMPILER", self.compiler.fc),
            self.define("METIS_ROOT", self.spec["metis"].prefix),
        ]
        if self.spec.satisfies("+mpi"):
            cmake_args.append(self.define("ParMETIS_ROOT", self.spec["parmetis"].prefix))
        cmake_args.append(self.cached_tests_work_dir)
        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        make = which("make")

        with working_dir(self.cached_tests_work_dir):
            cmake(*cmake_args)
            make()
            metis = which("metis")
            metis()
