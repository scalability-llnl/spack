# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Purify(CMakePackage):
    """PURIFY is an open-source collection of routines written in C++ available under the
    license below. It implements different tools and high-level to perform radio interferometric
    imaging, i.e. to recover images from the Fourier measurements taken by radio interferometric
    telescopes.
    """

    homepage = "https://astro-informatics.github.io/purify/"
    url = "https://github.com/astro-informatics/purify/archive/refs/tags/v4.2.0.tar.gz"
    git = "https://github.com/astro-informatics/purify"

    maintainers("tkoskela", "mmcleod89", "20DM")
    license("GPL-2.0")

    version("4.2.0", sha256="4d674007efc727628839fb6c8864e74f22adb39ee6405d3dab273f65b31b37e6")

    variant("tests", default=True, description="Build tests")
    variant("openmp", default=True, description="Enable multithreading with OpenMP")
    variant("mpi", default=True, description="Enable parallelisation with MPI")
    variant("benchmarks", default=False, description="Build benchmarks")
    variant("docs", default=False, description="Enable multithreading with OpenMP")
    variant("coverage", default=False, description="Enable code coverage")

    depends_on("cmake@3")
    depends_on("eigen@3.4:3")
    depends_on("libtiff@4.7:")
    depends_on("fftw-api")
    depends_on("yaml-cpp@0.7:")
    depends_on("boost@1.82+system+filesystem")
    depends_on("cfitsio@4")
    depends_on("cubature@1")
    depends_on("sopt~mpi", when="~mpi")
    depends_on("sopt+mpi", when="+mpi")
    depends_on("sopt~openmp", when="~openmp")
    depends_on("sopt+openmp", when="+openmp")
    depends_on("catch2@3.4:3", when="+tests")
    depends_on("mpi", when="+mpi")
    depends_on("benchmark@1.8~performance_counters", when="+benchmarks")
    depends_on("doxygen@1.9:1.12+graphviz", when="+docs")

    def cmake_args(self):
        args = [
            self.define_from_variant("docs", "docs"),
            self.define_from_variant("tests", "tests"),
            self.define_from_variant("benchmarks", "benchmarks"),
            self.define_from_variant("openmp", "openmp"),
            self.define_from_variant("dompi", "mpi"),
            self.define_from_variant("coverage", "coverage"),
        ]
        return args

    def setup_run_environment(self, env):
        if "+tests" in self.spec:
            env.prepend_path("PATH", self.spec.prefix.tests)
        if "+benchmarks" in self.spec:
            env.prepend_path("PATH", join_path(self.spec.prefix, "benchmarks"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")
            if "+tests" in spec:
                install_tree("cpp/tests", spec.prefix.tests)
                install_tree("data", join_path(spec.prefix, "data"))
            if "+benchmarks" in spec:
                install_tree("cpp/benchmarks", join_path(spec.prefix, "benchmarks"))
