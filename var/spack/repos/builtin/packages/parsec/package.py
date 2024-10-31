# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
import llnl.util.tty as tty

from spack.package import *


class Parsec(CMakePackage, CudaPackage):
    """PaRSEC: the Parallel Runtime Scheduler and Execution Controller

    PaRSEC is a runtime and a programming toolbox that support the design and
    parallel execution of micro-tasks on distributed, heterogeneous systems.
    """

    homepage = "https://icl.utk.edu/dte"
    git = "https://github.com/icldisco/parsec.git"
    url = "https://github.com/ICLDisco/parsec/archive/refs/tags/parsec-3.0.2012.tar.gz"
    list_url = "https://github.com/ICLDisco/parsec/tags"
    maintainers("abouteiller", "bosilca", "herault")
    tags = ["e4s"]

    test_requires_compiler = True

    license("BSD-3-Clause-Open-MPI")

    version("master", branch="master")
    version(
        "3.0.2209",
        sha256="67d383d076991484cb2a265f56420abdea7cc1f329c63ac65a3e96fbfb6cc295",
        url="https://bitbucket.org/icldistcomp/parsec/get/parsec-3.0.2209.tar.bz2",
    )
    version(
        "3.0.2012",
        sha256="f565bcfffe106be8237b6aea3e83a5770607b7236606414b6f270244fa6ec3bc",
        url="https://bitbucket.org/icldistcomp/parsec/get/parsec-3.0.2012.tar.bz2",
    )
    version(
        "1.1.0",
        sha256="d2928033c121000ae0a554f1e7f757c1f22274a8b74457ecd52744ae1f70b95a",
        url="https://bitbucket.org/icldistcomp/parsec/get/v1.1.0.tar.bz2",
    )

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    variant("shared", default=True, description="Build a shared library")
    variant("cuda", default=True, description="Build with CUDA")
    variant("profile", default=False, description="Generate profiling data")
    variant(
        "debug_verbose",
        default=False,
        description="Debug version with verbose and paranoid (incurs performance overhead!)",
    )
    conflicts(
        "+debug_verbose build_type=Release",
        msg="You need to set build_type=Debug for +debug_verbose",
    )
    conflicts(
        "+debug_verbose build_type=RelWithDebInfo",
        msg="You need to set build_type=Debug for +debug_verbose",
    )
    # TODO: Spack does not handle cross-compilation atm
    # variant('xcompile', default=False, description='Cross compile')

    depends_on("cmake@3.18:", type="build")
    depends_on("python", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("hwloc")
    depends_on("mpi")
    depends_on("papi", when="+profile")
    depends_on("python", type=("build", "run"), when="+profile")
    depends_on("py-cython", type=("build", "run"), when="+profile")
    depends_on("py-pandas", type=("build", "run"), when="+profile")
    depends_on("py-matplotlib", type=("build", "run"), when="+profile")
    depends_on("py-tables", type=("build", "run"), when="+profile")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PARSEC_GPU_WITH_CUDA", "cuda"),
            self.define_from_variant("PARSEC_PROF_TRACE", "profile"),
            self.define_from_variant("PARSEC_DEBUG_HISTORY", "debug_verbose"),
            self.define_from_variant("PARSEC_DEBUG_PARANOID", "debug_verbose"),
        ]
        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check(self):
        """Run ctest after building binary."""
        with working_dir(self.build_directory):
            try:
                ctest("--output-on-failure", "-j1")
            except ProcessError:
                warn = "ctest tests failed.\n"
                warn += "Please report this failure to:\n"
                warn += "https://bitbucket.org/icldistcomp/parsec/issues"
                tty.msg(warn)

    contrib_dir = join_path("contrib", "build_with_parsec")

    def test_contrib(self):
        """build and run contrib examples"""
        with working_dir(join_path(self.test_suite.current_test_cache_dir, self.contrib_dir)):
            cmake = self.spec["cmake"].command
            args = [
                "-Wno-dev",
                f"-DCMAKE_C_COMPILER={self.spec['mpi'].mpicc}",
                f"-DCMAKE_PREFIX_PATH={self.prefix}",
                ".",
            ]
            if "+cuda" in self.spec:
                args.append("-DCUDA_TOOLKIT_ROOT_DIR:STRING=" + self.spec["cuda"].prefix)

            cmake(*args)
            make()

            for name in ["dtd_test_allreduce", "write_check"]:
                with test_part(self, f"test_contrib_{name}", f"run {name}"):
                    exe = which(name)
                    exe()

    @run_after("install")
    def cache_test_sources(self):
        cache_extra_test_sources(self, self.contrib_dir)
