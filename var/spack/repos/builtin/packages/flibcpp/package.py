# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flibcpp(CMakePackage):
    """Fortran bindings to the C++ Standard Library."""

    homepage = "https://flibcpp.readthedocs.io/en/latest"
    git = "https://github.com/swig-fortran/flibcpp.git"
    url = "https://github.com/swig-fortran/flibcpp/archive/v1.0.1.tar.gz"

    test_requires_compiler = True

    license("MIT")

    version("1.0.2", sha256="e2c11c1f58ca830eb7ac7f25d66fc3502c4a8d994192ee30c63a1c3b51aac241")
    version("1.0.1", sha256="8569c71eab0257097a6aa666a6d86bdcb6cd6e31244d32cc5b2478d0e936ca7a")
    version("0.5.2", sha256="b9b4eb6431d5b56a54c37f658df7455eafd3d204a5534903b127e0c8a1c9b827")
    version("0.5.1", sha256="76db24ce7893f19ab97ea7260c39490ae1bd1e08a4cc5111ad7e70525a916993")
    version("0.5.0", sha256="94204198304ba4187815431859e5958479fa651a6f06f460b099badbf50f16b2")
    version("0.4.1", sha256="5c9a11af391fcfc95dd11b95338cff19ed8104df66d42b00ae54f6cde4da5bdf")
    version("0.4.0", sha256="ccb0acf58a4480977fdb3c62a0bd267297c1dfa687a142ea8822474c38aa322b")
    version("0.3.1", sha256="871570124122c18018478275d5040b4b787d1966e50ee95b634b0b5e0cd27e91")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("doc", default=False, description="Build and install documentation")
    variant("shared", default=True, description="Build shared libraries")
    variant("swig", default=False, description="Regenerate source files using SWIG")
    variant(
        "fstd",
        default="03",
        values=("none", "03", "08", "15", "18"),
        multi=False,
        description="Build with this Fortran standard",
    )

    depends_on("swig@4.0.2-fortran", type="build", when="+swig")
    depends_on("py-sphinx", type="build", when="+doc")

    @run_before("cmake")
    def die_without_fortran(self):
        # Until we can pass compiler requirements through virtual
        # dependencies, explicitly check for Fortran compiler instead of
        # waiting for configure error.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError("Flibcpp requires a Fortran compiler")

    def cmake_args(self):
        from_variant = self.define_from_variant
        fstd_key = (
            "FLIBCPP_Fortran_STANDARD"
            if self.version > Version("1.0.0")
            else "FLIBCPP_FORTRAN_STD"
        )
        return [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("FLIBCPP_BUILD_DOCS", "doc"),
            from_variant(fstd_key, "fstd"),
            from_variant("FLIBCPP_USE_SWIG", "swig"),
            self.define("FLIBCPP_BUILD_TESTS", bool(self.run_tests)),
            self.define("FLIBCPP_BUILD_EXAMPLES", bool(self.run_tests)),
        ]

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

    def test_examples(self):
        """build and run examples"""
        cmake_args = [
            self.define("CMAKE_PREFIX_PATH", self.prefix),
            self.define("CMAKE_Fortran_COMPILER", self.compiler.fc),
        ]
        cmake_args.append(self.cached_tests_work_dir)
        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        make = which("make")
        sh = which("sh")

        with working_dir(self.cached_tests_work_dir):
            cmake(*cmake_args)
            make()
            sh("run-examples.sh")
