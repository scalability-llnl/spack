# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class HypreCmake(CMakePackage, CudaPackage):
    """Hypre is a library of high performance preconditioners that
    features parallel multigrid methods for both structured and
    unstructured grid problems."""

    homepage = "http://computing.llnl.gov/project/linear_solvers/software.php"
    url = "https://github.com/hypre-space/hypre/archive/v2.14.0.tar.gz"
    git = "https://github.com/hypre-space/hypre.git"

    maintainers("ulrikeyang", "osborn9", "balay")

    test_requires_compiler = True

    version("develop", branch="master")
    version("2.22.0", sha256="2c786eb5d3e722d8d7b40254f138bef4565b2d4724041e56a8fa073bda5cfbb5")

    variant(
        "shared",
        default=(sys.platform != "darwin"),
        description="Build shared library (disables static library)",
    )
    variant(
        "superlu_dist", default=False, description="Activates support for SuperLU_Dist library"
    )
    variant("int64", default=False, description="Use 64bit integers")
    variant("mixedint", default=False, description="Use 64bit integers while reducing memory use")
    variant("complex", default=False, description="Use complex values")
    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("debug", default=False, description="Build debug instead of optimized version")
    variant("unified_memory", default=False, description="Use unified memory")

    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("superlu-dist", when="+superlu_dist+mpi")

    conflicts("+cuda", when="+int64")
    conflicts("+unified_memory", when="~cuda")

    def url_for_version(self, version):
        if version >= Version("2.12.0"):
            url = "https://github.com/hypre-space/hypre/archive/v{0}.tar.gz"
        else:
            url = "http://computing.llnl.gov/project/linear_solvers/download/hypre-{0}.tar.gz"

        return url.format(version)

    root_cmakelists_dir = "src"

    def cmake_args(self):
        from_variant = self.define_from_variant
        args = [
            from_variant("HYPRE_WITH_MPI", "mpi"),
            from_variant("HYPRE_WITH_OPENMP", "openmp"),
            from_variant("HYPRE_WITH_BIGINT", "int64"),
            from_variant("HYPRE_WITH_MIXEDINT", "mixedint"),
            from_variant("HYPRE_WITH_COMPLEX", "complex"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("HYPRE_ENABLE_SHARED", "shared"),
            from_variant("HYPRE_WITH_DSUPERLU", "superlu_dist"),
            from_variant("HYPRE_WITH_CUDA", "cuda"),
            from_variant("HYPRE_ENABLE_UNIFIED_MEMORY", "unified_memory"),
        ]

        return args

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
            env.set("CUDA_PATH", self.spec["cuda"].prefix)
            cuda_arch = self.spec.variants["cuda_arch"].value
            if cuda_arch:
                arch_sorted = list(sorted(cuda_arch, reverse=True))
                env.set("HYPRE_CUDA_SM", arch_sorted[0])
            # In CUDA builds hypre currently doesn't handle flags correctly
            env.append_flags("CXXFLAGS", "-O2" if "~debug" in self.spec else "-g")

    extra_install_tests = join_path("src", "examples")

    @run_after("install")
    def cache_test_sources(self):
        if "+mpi" not in self.spec:
            print("Package must be installed with +mpi to cache test sources")
            return
        # Customize the examples makefile before caching it
        makefile = join_path(self.extra_install_tests, "Makefile")
        filter_file(r"^HYPRE_DIR\s* =.*", f"HYPRE_DIR = {self.prefix}", makefile)
        filter_file(r"^CC\s*=.*", "CC = " + self.spec["mpi"].mpicc, makefile)
        filter_file(r"^F77\s*=.*", "F77 = " + self.spec["mpi"].mpif77, makefile)
        filter_file(r"^CXX\s*=.*", "CXX = " + self.spec["mpi"].mpicxx, makefile)
        filter_file(
            r"^LIBS\s*=.*",
            f"LIBS = -L$(HYPRE_DIR)/lib64 -lHYPRE -lm $(CUDA_LIBS) $(DOMP_LIBS)",
            makefile,
        )

        self.cache_extra_test_sources(self.extra_install_tests)

    @property
    def _cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir, self.extra_install_tests)

    def test_bigint(self):
        """build and run bigint tests"""
        if "+mpi" not in self.spec:
            raise SkipTest("Package must be installed with +mpi")

        # Build copied and cached test examples
        with working_dir(self._cached_tests_work_dir):
            make = which("make")
            make("bigint")

            # Run the examples built above
            for _bin in ["ex5big", "ex15big"]:
                with test_part(self, f"test_bigint_{_bin}", purpose=f"ensuring {_bin} runs"):
                    if not os.path.isfile(_bin):
                        raise SkipTest(f"{_bin} is missing")

                    exe = which(_bin)
                    exe()

    @property
    def headers(self):
        """Export the main hypre header, HYPRE.h; all other headers can be found
        in the same directory.
        Sample usage: spec['hypre'].headers.cpp_flags
        """
        hdrs = find_headers("HYPRE", self.prefix.include, recursive=False)
        return hdrs or None

    @property
    def libs(self):
        """Export the hypre library.
        Sample usage: spec['hypre'].libs.ld_flags
        """
        is_shared = "+shared" in self.spec
        libs = find_libraries("libHYPRE", root=self.prefix, shared=is_shared, recursive=True)
        return libs or None
